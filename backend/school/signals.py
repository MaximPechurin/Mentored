import logging

from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


def grant_course_access_for_order(order):
    """
    Выдаёт доступ (Enrollment) к учебным курсам по оплаченному заказу.

    Идемпотентно: срабатывает на каждом сохранении заказа со статусом
    'paid' (и вебхук Mercado Pago, и ручная смена статуса в админке),
    но доступ создаётся только если его ещё нет - существующие
    Enrollment не трогаются (в т.ч. если админ вручную снял is_active,
    повторное сохранение заказа его НЕ реактивирует).

    Резолв товара: OrderItem хранит product_type (имя модели в нижнем
    регистре, напр. 'course') и product_id. Ищем ContentType строго в
    app_label='mentored' - модель 'course' есть и в school, нельзя
    перепутать. По найденному товару берём все ProductCourseAccess и на
    каждый связанный курс заводим Enrollment.
    """
    from .models import ProductCourseAccess, Enrollment

    if order.status != 'paid':
        return

    for item in order.items.all():
        if not item.product_type or not item.product_id:
            continue
        try:
            ct = ContentType.objects.get(app_label='mentored', model=item.product_type)
        except ContentType.DoesNotExist:
            continue

        links = ProductCourseAccess.objects.filter(
            content_type=ct, object_id=item.product_id,
        ).select_related('course')

        for link in links:
            enrollment, created = Enrollment.objects.get_or_create(
                user=order.user,
                course=link.course,
                defaults={'order_item': item, 'is_active': True},
            )
            if created:
                logger.info(
                    "School: выдан доступ user=%s course=%s (заказ %s)",
                    order.user_id, link.course_id, order.order_number,
                )
                # письмо "доступ открыт" - best-effort, не роняет вебхук.
                # Роль student гарантируется отдельным сигналом на самом
                # Enrollment (см. on_enrollment_saved) - срабатывает и
                # тут, и при ручном создании доступа из админки.
                from .emails import send_course_access_granted
                send_course_access_granted(order.user, link.course)


def on_order_saved(sender, instance, **kwargs):
    """
    Обработчик post_save для mentored.Order. Никогда не роняет
    сохранение заказа / вебхук оплаты - ошибка выдачи доступа только
    логируется (вебхук Mercado Pago обязан быстро вернуть 200).
    """
    try:
        grant_course_access_for_order(instance)
    except Exception:
        logger.exception(
            "School: ошибка выдачи доступа по заказу %s",
            getattr(instance, 'order_number', '?'),
        )


def on_enrollment_saved(sender, instance, **kwargs):
    """
    Обработчик post_save для school.Enrollment. Гарантирует роль student
    у пользователя, если у него есть активный доступ к курсу - иначе
    доступ формально есть, а API школы (permission IsStudent) и кнопка
    "Ir a la Escuela" на фронте (смотрят на роль, не на Enrollment)
    ведут себя так, будто доступа нет.

    Срабатывает НЕЗАВИСИМО от того, как создан Enrollment - через оплату
    заказа (см. grant_course_access_for_order) или вручную из админки
    (штатный способ, см. докстринг Enrollment) - раньше роль
    проставлялась только в первом случае.
    """
    if not instance.is_active:
        return
    try:
        from mentored.models import Role
        student_role, _ = Role.objects.get_or_create(
            codename=Role.STUDENT, defaults={'name': 'Студент'},
        )
        instance.user.roles.add(student_role)
    except Exception:
        logger.exception(
            "School: ошибка назначения роли student для user=%s (enrollment=%s)",
            instance.user_id, instance.pk,
        )
