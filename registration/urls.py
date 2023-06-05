from django.urls import path

from . import views

urlpatterns = [
    path("product/registration", views.registrationRequest.as_view(), name='Registration'),
    path("product/application/<str:pk>", views.myApplications.as_view(), name='applications'),
    path("productClass", views.ProductClass.as_view(), name='productClass'),
    path("manufacturer/particulars/<str:pk>", views.ManufacturesParticulars, name='ManufacturesParticulars'),
    path("product/details/<str:pk>",views.productDetails.as_view(),name='productDetails'),
    path("active/ingredients/<str:pk>",views.Ingredients,name='Ingredients'),
    path("country/registered/<str:pk>",views.CountryRegistered,name='CountryRegistered'),
    path("marketing/authorization/<str:pk>",views.MarketingAuthorization,name='MarketingAuthorization'),
    path("makePayment/<str:pk>",views.makePayment.as_view(),name='makePayment'),
    path("my/submissions", views.allApplications.as_view(), name='allApplications'),
    path("submit/<str:pk>", views.SubmitRegistration, name='SubmitRegistration'),
    path("Attachement/<str:pk>", views.Attachement, name='Attachement'),
    path("GenerateCertificate/<str:pk>", views.GenerateCertificate, name='GenerateCertificate'),
    path("FnDeleteDocumentAttachment/<str:pk>", views.FnDeleteDocumentAttachment, name='FnDeleteDocumentAttachment'),
    path("FnRegulatory/<str:pk>", views.FnRegulatory, name='FnRegulatory'),

]