from django.urls import path

from . import views

urlpatterns = [
    path("biocidal/registration/<str:pk>", views.biocidalRegistration, name='biocidalRegistration'),
]