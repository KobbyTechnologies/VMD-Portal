from django.urls import path

from . import views

urlpatterns = [
    path("retention", views.registrationRetention.as_view(), name='retention'),
    path("retentionDetails/<str:pk>",views.retentionDetails.as_view(),name='retentionDetails'),
    path("retentionGateway/<str:pk>",views.retentionGateway.as_view(),name='retentionGateway'),
    path("SubmitRetention/<str:pk>",views.SubmitRetention,name='SubmitRetention'),
    path("makeRetentionPayment/<str:pk>",views.makeRetentionPayment.as_view(),name='makeRetentionPayment'),
    path("FNGenerateRetentionInvoice/<str:pk>",views.FNGenerateRetentionInvoice,name='FNGenerateRetentionInvoice'),
    path("PrintRentetionCertificate/<str:pk>",views.PrintRentetionCertificate,name='PrintRentetionCertificate'),
    path("FnRetentionAttachement/<str:pk>", views.FnRetentionAttachement, name="FnRetentionAttachement"),
]