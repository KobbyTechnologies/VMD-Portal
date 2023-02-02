from django.urls import path
from . import views

urlpatterns = [
    path('GMP', views.GMPApplication.as_view(), name='gmp'),
    path('GMPDetails/<str:pk>', views.GMPDetails.as_view(), name='GMPDetails'),
    path('GMPManufactures/<str:pk>', views.GMPManufactures, name='GMPManufactures'),
    path('linesToInspect/<str:pk>', views.linesToInspect, name='linesToInspect'),
    path('GMPGateway/<str:pk>', views.GMPGateway.as_view(), name='GMPGateway'),
    path('SubmitGMP/<str:pk>', views.SubmitGMP, name='SubmitGMP'),
    path('GMPAttachement/<str:pk>', views.GMPAttachement, name='GMPAttachement'),
    path('FnDeleteGMPDocumentAttachment/<str:pk>', views.FnDeleteGMPDocumentAttachment, name='FnDeleteGMPDocumentAttachment'),
    path('FNGenerateGMPInvoice/<str:pk>', views.FNGenerateGMPInvoice, name='FNGenerateGMPInvoice'),
]