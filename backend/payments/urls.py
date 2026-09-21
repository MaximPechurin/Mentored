from django.urls import path
from . import views

urlpatterns = [
    path('create-preference/', views.CreatePaymentPreferenceView.as_view(), name='create_preference'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
    # «Магическая ссылка» — быстрая покупка одного товара без регистрации.
    path('quick-buy/', views.QuickBuyView.as_view(), name='quick_buy'),
    path(
        'quick-buy/product/<str:product_type>/<str:slug>/',
        views.QuickBuyProductView.as_view(),
        name='quick_buy_product',
    ),
]
