from django.urls import path

from . import views

urlpatterns = [
    path("PaymentGateway", views.PaymentGateway, name='PaymentGateway'),
]