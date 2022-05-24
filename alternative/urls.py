from django.urls import path
from . import views

urlpatterns = [
    path("alternativeRegistration", views.alternativeRegistration, name='alternativeRegistration'),
]