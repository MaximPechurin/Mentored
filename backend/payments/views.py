import mercadopago
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from mentored.models import Cart, CartItem, Order

# Инициализируем SDK с ACCESS_TOKEN
sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)


class CreatePaymentPreferenceView(APIView):
    """POST /payment/create/ — создать предпочтение для оплаты"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or cart.items.count() == 0:
            return Response(
                {'error': 'Корзина пуста'},
                status=400
            )

        # Создаём заказ
        #from backend.mentored.views import CreateOrderView
        #order_view = CreateOrderView()
        #order_response = order_view.post(request)
        #if order_response.status_code != 201:
        #    return order_response

        order = Order.objects.get(
            user=request.user,
            cart=cart,
            status='pending'
        )

        # Формируем данные для Mercado Pago
        items = []
        for item in cart.items.all():
            product = item.product
            items.append({
                "id": str(product.id),
                "title": product.name[:255],
                "quantity": item.quantity,
                "unit_price": float(product.price),
                "currency_id": "BRL",
            })

        # Ссылки для возврата
        frontend_url = request.build_absolute_uri('/').replace('api.', '').replace(':8000', ':5173')
        back_urls = {
            "success": f"{frontend_url}/payment/success?order={order.order_number}",
            "failure": f"{frontend_url}/payment/failure",
            "pending": f"{frontend_url}/payment/pending",
        }

        preference_data = {
            "items": items,
            "back_urls": back_urls,
            "auto_return": "approved",
            "notification_url": request.build_absolute_uri('/payment/webhook/'),
            "external_reference": order.order_number,
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        # Сохраняем transaction_id в заказ
        order.transaction_id = preference.get("id")
        order.save()

        return Response({
            "init_point": preference["init_point"],
            "order_number": order.order_number,
        })


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
