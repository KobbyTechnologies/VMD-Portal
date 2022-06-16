from django.urls import path

from . import views

urlpatterns = [
    path("product/registration", views.registrationRequest, name='Registration'),
    path("product/application/<str:pk>", views.myApplications, name='applications'),
    path("registrationRenewal", views.registrationRenewal, name='renewal'),
    path("productClass", views.productClass, name='productClass'),
]