from django.urls import path

from . import views

urlpatterns = [
    path("payment/gateway/<str:pk>", views.PaymentGateway, name='PaymentGateway'),
]