from django.urls import path

from . import views

urlpatterns = [
    path("product/registration", views.registrationRequest, name='Registration'),
    path("product/application/<str:pk>", views.myApplications, name='applications'),
    path("registrationRenewal", views.registrationRenewal, name='renewal'),
    path("productClass", views.productClass, name='productClass'),
    path("manufacturer/particulars/<str:pk>", views.ManufacturesParticulars, name='ManufacturesParticulars'),
    path("product/details/<str:pk>",views.productDetails,name='productDetails'),
    path("active/ingredients/<str:pk>",views.activeIngredients,name='activeIngredients'),
    path("inactive/ingredients/<str:pk>",views.InactiveIngredients,name='InactiveIngredients'),
    path("country/registered/<str:pk>",views.CountryRegistered,name='CountryRegistered'),
    path("marketing/authorization/<str:pk>",views.MarketingAuthorization,name='MarketingAuthorization'),
]