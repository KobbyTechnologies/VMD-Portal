from django.urls import path

from . import views

urlpatterns = [
    path("devices/registration/<str:pk>", views.devicesRegistration, name='devicesRegistration'),
    path("essential/principles/<str:pk>", views.essentialPrinciples, name='essentialPrinciples'),
    path("FnDeviceAttachement/<str:pk>", views.FnDeviceAttachement, name='FnDeviceAttachement'),
]