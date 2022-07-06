from django.urls import path

from . import views

urlpatterns = [
    path("retention", views.registrationRetention, name='retention'),
    path("ApplyRetention/<str:pk>/<str:id>",views.ApplyRetention,name='ApplyRetention'),
    path("retentionDetails/<str:pk>",views.retentionDetails,name='retentionDetails'),
    path("retentionGateway/<str:pk>",views.retentionGateway,name='retentionGateway'),
    path("SubmitRetention/<str:pk>",views.SubmitRetention,name='SubmitRetention'),
]