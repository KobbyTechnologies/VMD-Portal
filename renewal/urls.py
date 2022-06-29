from django.urls import path

from . import views

urlpatterns = [
    path("renew", views.RenewalRequest, name='renew'),
]