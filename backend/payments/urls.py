from django.urls import path
from . import views

urlpatterns = [
    path('create-preference/', views.CreatePaymentPreferenceView.as_view(), name='create_preference'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
]