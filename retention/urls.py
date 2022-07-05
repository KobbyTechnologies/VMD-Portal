from django.urls import path

from . import views

urlpatterns = [
    path("retention", views.registrationRetention, name='retention'),
    path("ApplyRetention/<str:pk>",views.ApplyRetention,name='ApplyRetention'),
    path("retentionDetails/<str:pk>",views.retentionDetails,name='retentionDetails'),
    path("retentionPayment/<str:pk>/<str:id>",views.retentionPayment,name='retentionPayment'),
    path("retentionGateway/<str:pk>",views.retentionGateway,name='retentionGateway'),
]