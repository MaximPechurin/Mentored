from django.apps import AppConfig


class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school'
    verbose_name = 'Школа: курсы и обучение'

    def ready(self):
        # Хук "оплата -> доступ": слушаем сохранение mentored.Order и на
        # статусе 'paid' выдаём Enrollment. Подключаем здесь (а не через
        # @receiver со строковым sender), чтобы модель точно была
        # загружена и не было проблем с порядком импорта.
        from django.db.models.signals import post_save
        from mentored.models import Order
        from .models import Enrollment
        from . import signals
        post_save.connect(signals.on_order_saved, sender=Order, dispatch_uid='school_grant_access')
        # Роль student гарантируется на самом Enrollment - работает и
        # при выдаче доступа через оплату, и при ручном создании из
        # админки (см. докстринг on_enrollment_saved).
        post_save.connect(signals.on_enrollment_saved, sender=Enrollment, dispatch_uid='school_ensure_student_role')
