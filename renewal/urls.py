from django.urls import path

from . import views

urlpatterns = [
    path("renew", views.RenewalRequest, name='renew'),
    path("ApplyRenewal/<str:pk>", views.ApplyRenewal, name='ApplyRenewal'),
]