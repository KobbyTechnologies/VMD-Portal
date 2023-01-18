from django.urls import path

from . import views

urlpatterns = [
    path("variation", views.variation.as_view(), name='variation'),
    path("variationDetails/<str:pk>",views.variationDetails.as_view(),name='variationDetails'),
    path("variationGateway/<str:pk>",views.variationGateway.as_view(),name='variationGateway'),
    path("SubmitVariation/<str:pk>",views.SubmitVariation,name='SubmitVariation'),
    path("FnRetentionAttachement/<str:pk>", views.FnRetentionAttachement, name="FnRetentionAttachement"),
]