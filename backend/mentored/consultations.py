"""
Логика консультаций: слоты, бронирование, сериализация.
"""
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import ConsultationSlot, ConsultationBooking


SLOT_RESERVE_MINUTES = 15


def release_expired_slots(mentor=None):
    """
    Освобождает слоты, у которых истёк reserved_until.
    Вызывается при каждом запросе доступных слотов (без Celery)
    и опционально management-командой.
    """
    now = timezone.now()
    qs = ConsultationSlot.objects.filter(
        is_booked=True,
        reserved_until__lt=now,
    )
    if mentor:
        qs = qs.filter(mentor=mentor)

    # У этих слотов бронь либо pending, либо отсутствует.
    # Освобождаем сам слот, бронь отменяем.
    for slot in qs:
        booking = getattr(slot, 'booking', None)
        if booking and booking.status == 'pending':
            booking.status = 'cancelled'
            booking.save(update_fields=['status'])
        slot.is_booked = False
        slot.reserved_until = None
        slot.save(update_fields=['is_booked', 'reserved_until'])


@transaction.atomic
def reserve_slot(slot_id, user, consultation, **client_data):
    """
    Резервирует слот на SLOT_RESERVE_MINUTES минут и создаёт booking(pending).
    Бросает SlotUnavailableError, если слот занят.
    """
    now = timezone.now()

    # select_for_update — блокируем строку на время транзакции
    slot = ConsultationSlot.objects.select_for_update().get(pk=slot_id)

    # Если слот занят, но резерв истёк — освобождаем
    if slot.is_booked and slot.reserved_until and slot.reserved_until <= now:
        slot.is_booked = False
        slot.reserved_until = None
        slot.save(update_fields=['is_booked', 'reserved_until'])

    if slot.is_booked:
        raise SlotUnavailableError('Este horario ya está reservado.')

    # Резервируем
    slot.is_booked = True
    slot.reserved_until = now + timedelta(minutes=SLOT_RESERVE_MINUTES)
    slot.save(update_fields=['is_booked', 'reserved_until'])

    # Создаём booking
    booking = ConsultationBooking.objects.create(
        user=user,
        consultation=consultation,
        mentor=slot.mentor,
        slot=slot,
        scheduled_at=slot.starts_at,
        status='pending',
        amount_usd=consultation.price,
        client_name=client_data.get('client_name', ''),
        client_email=client_data.get('client_email', user.email),
        client_whatsapp=client_data.get('client_whatsapp', ''),
        client_country=client_data.get('client_country', ''),
        client_whatsapp=client_data.get('client_whatsapp', ''),
        topic=client_data.get('topic', ''),
        timezone=client_data.get('timezone', ''),
    )
    return booking


class SlotUnavailableError(Exception):
    pass