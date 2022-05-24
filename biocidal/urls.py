from django.urls import path

from . import views

urlpatterns = [
    path("biocidalRegistration", views.biocidalRegistration, name='biocidalRegistration'),
]