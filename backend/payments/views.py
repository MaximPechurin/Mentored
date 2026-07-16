#import mercadopago УСТАНОВИТЬ
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Инициализируем SDK с твоим ACCESS_TOKEN
#sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)


class CreatePreferenceView(View):
    """Создаёт предпочтение (Preference) для Checkout Pro"""

    def get(self, request):
        # Данные о товаре (в будущем ты будешь брать их из корзины)
        preference_data = {
            "items": [
                {
                    "title": "Mi producto",  # Название товара
                    "quantity": 1,
                    "unit_price": 100,  # Цена в местной валюте
                }
            ],
            # Куда вернуть пользователя после успешной оплаты
            "back_urls": {
                "success": "http://localhost:8000/payment/success/",
                "failure": "http://localhost:8000/payment/failure/",
                "pending": "http://localhost:8000/payment/pending/",
            },
            "auto_return": "approved",  # Автоматически возвращать после успеха
            "notification_url": "https://tu-сайт.ру/payment/webhook/"  # URL для уведомлений от MP
        }

        # Отправляем запрос в Mercado Pago
        preference_response = '1'#sdk.preference().create(preference_data)
        preference = preference_response["response"]
        # У пользователя будет кнопка "Оплатить", которая ведёт на init_point
        return JsonResponse({"init_point": preference["init_point"]})


@csrf_exempt  # Отключаем CSRF для внешних запросов от Mercado Pago
def payment_webhook(request):
    """Обрабатывает уведомления от Mercado Pago (Webhook)"""
    if request.method == "POST":
        # Получаем ID платежа из уведомления
        payment_id = request.GET.get('data.id')
        if payment_id:
            # Запрашиваем статус платежа
            payment_response = '1'#sdk.payment().get(payment_id)
            payment = payment_response["response"]
            status = payment.get("status")

            # Логика в зависимости от статуса
            if status == "approved":
                # Оплата прошла успешно!
                # Здесь потом ДОБАВИТЬ!!!:
                # 1. Обновить статус заказа в БД
                # 2. Очистить корзину пользователя
                # 3. Отправить письмо клиенту
                print(f"Платёж {payment_id} успешно завершён!")

            elif status == "cancelled":
                print(f"Платёж {payment_id} отменён.")
            elif status == "in_process":
                print(f"Платёж {payment_id} в процессе...")
            else:
                print(f"Платёж {payment_id} имеет статус: {status}")
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Метод не разрешён"}, status=405)
