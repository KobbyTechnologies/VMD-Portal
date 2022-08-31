from django.urls import path

from . import views

urlpatterns = [
    path("renew", views.RenewalRequest.as_view(), name='renew'),
    path("ApplyRenewal", views.ApplyRenewal.as_view(), name='ApplyRenewal'),
    path("renewDetails/<str:pk>", views.renewDetails.as_view(), name='renewDetails'),
    path("renewGateway/<str:pk>", views.renewGateway.as_view(), name='renewGateway'),
    path("SubmitRenewal/<str:pk>", views.SubmitRenewal, name='SubmitRenewal'),
    path("RenewAttachement/<str:pk>", views.RenewAttachement, name='RenewAttachement'),
]