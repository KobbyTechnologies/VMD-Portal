from django.urls import path

from . import views

urlpatterns = [
    path("pesticide/registration/<str:pk>", views.pesticideRegistration, name='pesticideRegistration'),
]