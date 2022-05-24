from django.urls import path

from . import views

urlpatterns = [
    path("devicesRegistration", views.devicesRegistration, name='devicesRegistration'),
]