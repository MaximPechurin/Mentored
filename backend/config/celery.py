"""
Инициализация Celery для проекта MENTORED.
Подхватывает настройки из Django settings с префиксом CELERY_.
Автоматически находит tasks.py во всех INSTALLED_APPS.
"""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('mentored')

# Все настройки Celery — из Django settings, с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим tasks.py во всех приложениях
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Тестовый таск — выводит свой request в логи."""
    print(f'Request: {self.request!r}')