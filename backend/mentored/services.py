"""
Сервис-слой «магической ссылки» (быстрая покупка одного товара без
предварительной регистрации).

Логика вынесена сюда из вьюх, чтобы её можно было переиспользовать и покрыть
тестами отдельно от HTTP-слоя. Сами HTTP-эндпоинты - в payments/views.py
(QuickBuyView, QuickBuyProductView), т.к. финальный шаг - создание preference
в Mercado Pago.

Идея потока: пользователь кликает по ссылке на конкретный товар, вводит только
email и жмёт «купить». По email мы находим существующий аккаунт или заводим
новый (со случайным паролем и ролью student). Заказ на 1 товар привязывается к
этому аккаунту - поэтому после оплаты уже существующий сигнал «оплата →
Enrollment» (school/signals.py) сам откроет доступ к учебному курсу, а заказ
будет виден в кабинете. Новому пользователю уходит письмо с паролем.
"""
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import transaction
from django.utils.crypto import get_random_string

from .models import Role, Order, OrderItem, Book, Course, Consultation, Membership

logger = logging.getLogger(__name__)
User = get_user_model()


# Те же типы товаров, что понимает корзина (CartAddItemView.model_map) - держим
# согласованным. Ключ - строковый product_type из запроса/URL.
PRODUCT_MODEL_MAP = {
    'course': Course,
    'book': Book,
    'consultation': Consultation,
    'membership': Membership,
}


class ProductNotFound(Exception):
    """Товар не найден / неизвестный тип / неактивен."""


def resolve_product(product_type, *, product_id=None, slug=None):
    """
    Находит активный товар по типу + (id ИЛИ slug). Для «магической ссылки»
    удобнее slug (читаемый URL), но поддерживаем и id.

    Возвращает (product, content_type). Бросает ProductNotFound.
    """
    model = PRODUCT_MODEL_MAP.get(product_type)
    if model is None:
        raise ProductNotFound(f'Неизвестный тип товара: {product_type}')

    lookup = {'is_active': True}
    if product_id not in (None, ''):
        lookup['id'] = product_id
    elif slug:
        lookup['slug'] = slug
    else:
        raise ProductNotFound('Не указан товар (нужен product_id или slug)')

    try:
        product = model.objects.get(**lookup)
    except (model.DoesNotExist, ValueError, TypeError):
        # ValueError/TypeError - если id пришёл нечисловой.
        raise ProductNotFound('Товар не найден')

    return product, ContentType.objects.get_for_model(model)


def _unique_username(email):
    """
    username у нас unique и отдельно от email (логин идёт по email, см.
    User.USERNAME_FIELD). Для гостя генерируем читаемый уникальный username из
    локальной части адреса, при коллизии - добавляем короткий суффикс.
    """
    base = (email.split('@')[0] or 'user')[:140] or 'user'
    username = base
    while User.objects.filter(username=username).exists():
        username = f'{base}-{get_random_string(4).lower()}'
    return username


@transaction.atomic
def get_or_create_buyer(email):
    """
    Находит пользователя по email (без учёта регистра) или создаёт нового со
    случайным паролем и ролью student.

    Возвращает (user, created, raw_password). raw_password - строка только для
    только что созданного пользователя (её надо отправить письмом); для
    существующего - None (пароль мы не знаем и не трогаем).
    """
    email = (email or '').strip().lower()

    user = User.objects.filter(email__iexact=email).first()
    if user is not None:
        return user, False, None

    raw_password = get_random_string(10)
    user = User(email=email, username=_unique_username(email))
    user.set_password(raw_password)
    user.save()

    student_role, _ = Role.objects.get_or_create(
        codename=Role.STUDENT, defaults={'name': 'Студент'},
    )
    user.roles.add(student_role)

    return user, True, raw_password


@transaction.atomic
def create_single_item_order(user, product, content_type):
    """
    Создаёт заказ (status='pending') на один экземпляр товара для пользователя.
    Повторяет ту же «заморозку» товара в OrderItem, что и обычный
    CreateOrderView, но без корзины (у гостя её нет).
    """
    order = Order.objects.create(
        user=user,
        total=product.price,
        is_digital=True,
        is_active=True,
        status='pending',
    )
    OrderItem.objects.create(
        order=order,
        product_type=content_type.model,
        product_id=product.id,
        product_name=product.name,
        product_price=product.price,
        quantity=1,
        total=product.price,
    )
    return order


def send_buyer_credentials(user, raw_password, *, login_url=None):
    """
    Best-effort письмо новому покупателю с логином/паролем.

    Пока SMTP не настроен (EMAIL_HOST_USER пуст) - тихо пропускаем (почтовый
    сервис подключает отдельный разработчик; здесь готовая точка вызова).
    Никогда не роняет покупку: любая ошибка почты только логируется.

    Возвращает True, если письмо отправлено.
    """
    if not settings.EMAIL_HOST_USER:
        logger.warning(
            'SMTP не настроен - письмо с доступом для %s не отправлено '
            '(покупка при этом прошла, аккаунт создан).', user.email,
        )
        return False

    login_url = login_url or 'https://www.mentoredgroup.com/login'
    try:
        send_mail(
            subject='Tu acceso a Mentored',
            message=(
                '¡Gracias por tu compra!\n\n'
                'Hemos creado tu cuenta para que puedas acceder al curso:\n'
                f'  Correo: {user.email}\n'
                f'  Contraseña: {raw_password}\n\n'
                f'Inicia sesión aquí: {login_url}\n'
                'Por seguridad, te recomendamos cambiar la contraseña después de entrar.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception:
        logger.exception('No se pudo enviar el correo de acceso a %s', user.email)
        return False
