from django.urls import path

from . import views

urlpatterns = [
    path("renew", views.RenewalRequest, name='renew'),
    path("ApplyRenewal/<str:pk>/<str:id>", views.ApplyRenewal, name='ApplyRenewal'),
    path("renewDetails/<str:pk>", views.renewDetails, name='renewDetails'),
    path("renewGateway/<str:pk>", views.renewGateway, name='renewGateway'),
    path("SubmitRenewal/<str:pk>", views.SubmitRenewal, name='SubmitRenewal'),
]