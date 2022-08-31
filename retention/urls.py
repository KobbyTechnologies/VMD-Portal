from django.urls import path

from . import views

urlpatterns = [
    path("retention", views.registrationRetention.as_view(), name='retention'),
    path("retentionDetails/<str:pk>",views.retentionDetails.as_view(),name='retentionDetails'),
    path("retentionGateway/<str:pk>",views.retentionGateway.as_view(),name='retentionGateway'),
    path("SubmitRetention/<str:pk>",views.SubmitRetention,name='SubmitRetention'),
]