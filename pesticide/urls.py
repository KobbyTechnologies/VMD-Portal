from django.urls import path

from . import views

urlpatterns = [
    path("pesticideRegistration", views.pesticideRegistration, name='pesticideRegistration'),
]