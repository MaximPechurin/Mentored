import hashlib
import hmac
import logging

import mercadopago
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from mentored.models import Order
from mentored.services import (
    resolve_product, get_or_create_buyer, create_single_item_order,
    send_buyer_credentials, ProductNotFound,
)
from .models import Payment

logger = logging.getLogger(__name__)


class PreferenceError(Exception):
    """Не удалось создать preference в Mercado Pago."""


def _frontend_base_url(request):
    """
    Базовый URL фронта. В деве бэкенд на :8000, фронт на :5173 - подменяем порт;
    в проде порта в host нет, замена ничего не делает.
    """
    return request.build_absolute_uri('/').rstrip('/').replace(':8000', ':5173')


def create_payment_preference(request, order):
    """
    Создаёт preference в Mercado Pago для заказа, заводит/обновляет Payment и
    возвращает init_point (ссылку на оплату Checkout Pro).

    Общий код для обычной оплаты (CreatePaymentPreferenceView) и «магической
    ссылки» (QuickBuyView). Бросает PreferenceError при любой неудаче -
    вызывающий сам решает, какой HTTP-ответ отдать.
    """
    if not order.items.exists():
        raise PreferenceError('В заказе нет товаров')

    items = [{
        "id": str(order_item.product_id),
        "title": order_item.product_name[:255],
        "quantity": order_item.quantity,
        "unit_price": float(order_item.product_price),
        "currency_id": settings.MERCADOPAGO_CURRENCY,
    } for order_item in order.items.all()]

    frontend_url = _frontend_base_url(request)
    back_urls = {
        "success": f"{frontend_url}/order/{order.order_number}?payment=success",
        "failure": f"{frontend_url}/order/{order.order_number}?payment=failure",
        "pending": f"{frontend_url}/order/{order.order_number}?payment=pending",
    }

    preference_data = {
        "items": items,
        "back_urls": back_urls,
        "auto_return": "approved",
        "notification_url": request.build_absolute_uri('/payment/webhook/'),
        "external_reference": order.order_number,
    }

    try:
        preference_response = sdk.preference().create(preference_data)
    except Exception:
        logger.exception("Mercado Pago: ошибка создания preference для заказа %s", order.order_number)
        raise PreferenceError('Не удалось создать платёж')

    preference = preference_response.get("response", {})
    preference_id = preference.get("id")
    init_point = preference.get("init_point")

    if preference_response.get("status") not in (200, 201) or not init_point:
        logger.error(
            "Mercado Pago: неожиданный ответ на создание preference (заказ %s): %s",
            order.order_number, preference_response,
        )
        raise PreferenceError('Не удалось создать платёж')

    # id preference храним как временный transaction_id, реальный payment id
    # перезапишется вебхуком после фактической оплаты.
    Payment.objects.update_or_create(
        order=order,
        defaults={
            'user': order.user,
            'transaction_id': preference_id,
            'amount': order.total,
            'status': 'pending',
        },
    )

    return init_point

# Инициализируем SDK с ACCESS_TOKEN
sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

# Статусы платежа Mercado Pago -> статус нашего заказа/платежа.
# https://www.mercadopago.com.br/developers/en/docs/checkout-pro/payment-notifications
MP_STATUS_TO_ORDER_STATUS = {
    'approved': 'paid',
    'pending': 'pending',
    'in_process': 'processing',
    'authorized': 'processing',
    'in_mediation': 'processing',
    'rejected': 'cancelled',
    'cancelled': 'cancelled',
    'refunded': 'refunded',
    'charged_back': 'refunded',
}

MP_STATUS_TO_PAYMENT_STATUS = {
    'approved': 'approved',
    'pending': 'pending',
    'in_process': 'pending',
    'authorized': 'pending',
    'in_mediation': 'pending',
    'rejected': 'rejected',
    'cancelled': 'cancelled',
    'refunded': 'refunded',
    'charged_back': 'refunded',
}


class CreatePaymentPreferenceView(APIView):
    """POST /payment/create-preference/ — создать предпочтение (preference) для оплаты в Checkout Pro.

    Тело запроса: {"order_number": "ORD-20260725-000001"} (опционально — если не
    передан, берётся последний pending-заказ юзера, для обратной совместимости).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # ВАЖНО: CreateOrderView переносит товары корзины в OrderItem и сразу же
        # очищает CartItem (mentored/views.py::CreateOrderView, "Очищаем корзину").
        # Поэтому к моменту оплаты корзина уже пустая - это ожидаемо, а не ошибка.
        # Товары для Mercado Pago берём из "замороженных" OrderItem, а не из корзины.
        order_number = request.data.get('order_number')
        order_qs = Order.objects.filter(user=request.user, status='pending')
        if order_number:
            order_qs = order_qs.filter(order_number=order_number)
        order = order_qs.order_by('-created_at').first()

        if not order:
            return Response({'error': 'Заказ не найден'}, status=404)

        try:
            init_point = create_payment_preference(request, order)
        except PreferenceError as exc:
            # «В заказе нет товаров» - это 400 (проблема данных заказа), всё
            # остальное - 502 (сбой на стороне платёжного шлюза).
            code = 400 if 'нет товаров' in str(exc) else 502
            msg = str(exc) if code == 400 else 'Не удалось создать платёж. Попробуйте позже.'
            return Response({'error': msg}, status=code)

        return Response({
            "init_point": init_point,
            "order_number": order.order_number,
        })


def _verify_mp_signature(request, data_id):
    """Проверяет заголовок x-signature по гайду Mercado Pago:
    https://www.mercadopago.com.br/developers/en/docs/your-integrations/notifications/webhooks

    Возвращает True, если подпись валидна ИЛИ секрет ещё не настроен (пока
    используются тестовые ключи и секрет вебхука не выдан — тогда просто
    пропускаем проверку, но пишем warning в лог).
    """
    secret = settings.MERCADOPAGO_WEBHOOK_SECRET
    if not secret:
        logger.warning(
            "MERCADOPAGO_WEBHOOK_SECRET не настроен — подпись вебхука не проверяется. "
            "Взять секрет: Your integrations -> приложение -> Webhooks -> Configure notifications."
        )
        return True

    x_signature = request.headers.get('x-signature', '')
    x_request_id = request.headers.get('x-request-id', '')
    if not x_signature:
        logger.warning("Webhook без заголовка x-signature — отклонён.")
        return False

    ts = None
    v1 = None
    for part in x_signature.split(','):
        if '=' not in part:
            continue
        key, value = part.split('=', 1)
        key = key.strip()
        value = value.strip()
        if key == 'ts':
            ts = value
        elif key == 'v1':
            v1 = value

    if not ts or not v1:
        logger.warning("Не удалось разобрать x-signature: %r", x_signature)
        return False

    manifest = f"id:{str(data_id).lower()};request-id:{x_request_id};ts:{ts};"
    computed = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed, v1):
        logger.warning("Неверная подпись вебхука Mercado Pago (data.id=%s).", data_id)
        return False

    return True


@csrf_exempt  # Отключаем CSRF для внешних запросов от Mercado Pago
def payment_webhook(request):
    """Обрабатывает уведомления от Mercado Pago (Webhook).

    MP шлёт data.id/type в query-параметрах даже у POST-запроса. Отвечаем 200
    максимально быстро и никогда не 500-им, иначе MP будет ретраить бесконечно.
    """
    if request.method not in ("POST", "GET"):
        return JsonResponse({"error": "Метод не разрешён"}, status=405)

    data_id = request.GET.get('data.id') or request.GET.get('id')
    topic = request.GET.get('type') or request.GET.get('topic')

    if not data_id:
        # Например, тестовый пинг без данных — просто подтверждаем получение.
        return JsonResponse({"status": "ok"})

    if topic not in (None, 'payment'):
        # merchant_order и прочие топики пока не обрабатываем.
        return JsonResponse({"status": "ignored"})

    if not _verify_mp_signature(request, data_id):
        return JsonResponse({"error": "invalid signature"}, status=401)

    try:
        payment_response = sdk.payment().get(data_id)
        payment = payment_response["response"]
    except Exception:
        logger.exception("Mercado Pago: не удалось получить платёж %s", data_id)
        # Отвечаем 200, чтобы MP не долбил ретраями по нашей внутренней ошибке
        # бесконечно, ошибка уже залогирована для ручного разбора.
        return JsonResponse({"status": "error logged"})

    mp_status = payment.get("status")
    order_number = payment.get("external_reference")

    order = Order.objects.filter(order_number=order_number).first()
    if not order:
        logger.error(
            "Webhook Mercado Pago: заказ %s не найден (payment_id=%s, status=%s)",
            order_number, data_id, mp_status,
        )
        return JsonResponse({"status": "order not found"})

    payment_status = MP_STATUS_TO_PAYMENT_STATUS.get(mp_status, 'pending')
    order_status = MP_STATUS_TO_ORDER_STATUS.get(mp_status, order.status)

    payment_obj, _ = Payment.objects.update_or_create(
        order=order,
        defaults={
            'user': order.user,
            'transaction_id': str(data_id),
            'amount': payment.get('transaction_amount') or order.total,
            'status': payment_status,
            'payment_method': payment.get('payment_method_id'),
            'payment_response': payment,
            'paid_at': timezone.now() if mp_status == 'approved' else None,
        },
    )

    order.status = order_status
    if mp_status == 'approved' and not order.paid_at:
        order.paid_at = timezone.now()
    order.save()

    logger.info("Webhook Mercado Pago: заказ %s -> %s (payment_id=%s)", order_number, order_status, data_id)
    return JsonResponse({"status": "ok"})


# ============================================================
# «МАГИЧЕСКАЯ ССЫЛКА» — быстрая покупка одного товара без регистрации
# ============================================================
class QuickBuyView(APIView):
    """
    POST /payment/quick-buy/ — покупка одного товара по прямой ссылке, без
    предварительной регистрации.

    Тело: {product_type, email, product_id | slug}.
      - product_type: 'course' | 'book' | 'consultation' | 'membership'
      - товар задаётся product_id ИЛИ slug (для читаемой ссылки удобнее slug)
      - email: куда привязать покупку (и куда отправить доступ новому клиенту)

    Что делает: находит/создаёт аккаунт по email, создаёт заказ на 1 товар и
    возвращает init_point (ссылку на оплату Mercado Pago). Доступ к учебному
    курсу после оплаты откроется автоматически (сигнал оплата → Enrollment).
    Новому пользователю уходит письмо с паролем (когда подключён SMTP).

    Публичный эндпоинт (ссылку встраивают на внешних площадках), поэтому стоит
    троттлинг от спама аккаунтами/письмами.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'quick_buy'

    def post(self, request):
        email = (request.data.get('email') or '').strip()
        product_type = request.data.get('product_type')
        product_id = request.data.get('product_id')
        slug = request.data.get('slug')

        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {'error': 'Introduce un correo electrónico válido.'},
                status=400,
            )

        try:
            product, content_type = resolve_product(
                product_type, product_id=product_id, slug=slug,
            )
        except ProductNotFound as exc:
            return Response({'error': str(exc)}, status=404)

        user, created, raw_password = get_or_create_buyer(email)
        order = create_single_item_order(user, product, content_type)

        try:
            init_point = create_payment_preference(request, order)
        except PreferenceError:
            # Заказ уже создан в статусе pending - оставляем, менеджер увидит
            # его в админке; пользователю показываем ошибку платежа.
            return Response(
                {'error': 'No se pudo iniciar el pago. Inténtalo de nuevo más tarde.'},
                status=502,
            )

        if created:
            send_buyer_credentials(
                user, raw_password, login_url=f"{_frontend_base_url(request)}/login",
            )

        # is_new_user отдаём, чтобы фронт мог показать нужную подсказку («мы
        # отправили доступ на почту» / «войдите под своим паролем»). Это слегка
        # раскрывает, был ли email в системе - осознанный компромисс ради UX.
        return Response({
            'init_point': init_point,
            'order_number': order.order_number,
            'is_new_user': created,
        })


class QuickBuyProductView(APIView):
    """
    GET /payment/quick-buy/product/<product_type>/<slug>/ — публичная карточка
    товара для лендинга «магической ссылки» (без авторизации): название, цена,
    описание, картинка. Фронт по ней рисует страницу до ввода email.
    """
    permission_classes = [AllowAny]

    def get(self, request, product_type, slug):
        from mentored.serializers import (
            BookSerializer, CourseSerializer, ConsultationSerializer, MembershipSerializer,
        )
        serializer_map = {
            'course': CourseSerializer,
            'book': BookSerializer,
            'consultation': ConsultationSerializer,
            'membership': MembershipSerializer,
        }
        try:
            product, _ = resolve_product(product_type, slug=slug)
        except ProductNotFound as exc:
            return Response({'error': str(exc)}, status=404)

        serializer_cls = serializer_map[product_type]
        return Response({
            'product_type': product_type,
            'product': serializer_cls(product, context={'request': request}).data,
        })
