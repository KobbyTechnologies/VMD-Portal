from django.urls import path

from . import views

urlpatterns = [
    path("product/registration", views.registrationRequest, name='Registration'),
    path("product/application/<str:pk>", views.myApplications, name='applications'),
    path("productClass", views.productClass, name='productClass'),
    path("manufacturer/particulars/<str:pk>", views.ManufacturesParticulars, name='ManufacturesParticulars'),
    path("product/details/<str:pk>",views.productDetails,name='productDetails'),
    path("active/ingredients/<str:pk>",views.Ingredients,name='Ingredients'),
    path("country/registered/<str:pk>",views.CountryRegistered,name='CountryRegistered'),
    path("marketing/authorization/<str:pk>",views.MarketingAuthorization,name='MarketingAuthorization'),
    path("makePayment/<str:pk>",views.makePayment,name='makePayment'),
    path("my/submissions", views.allApplications, name='allApplications'),
    path("submit/<str:pk>", views.SubmitRegistration, name='SubmitRegistration'),
    path("Attachement/<str:pk>", views.Attachement, name='Attachement'),
    path("GenerateCertificate/<str:pk>", views.GenerateCertificate, name='GenerateCertificate'),

]