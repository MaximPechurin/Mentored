from celery import shared_task
from django.utils import timezone

@shared_task(name='mentored.debug_heartbeat')
def debug_heartbeat():
    return f'Heartbeat at {timezone.now().isoformat()}'