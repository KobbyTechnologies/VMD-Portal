from django.urls import path

from . import views

urlpatterns = [
    path("variation", views.variation, name='variation'),
    path("ApplyVariation",views.ApplyVariation,name='ApplyVariation'),
    path("variationDetails/<str:pk>",views.variationDetails,name='variationDetails'),
    path("variationGateway/<str:pk>",views.variationGateway,name='variationGateway'),
    path("SubmitVariation/<str:pk>",views.SubmitVariation,name='SubmitVariation'),
]