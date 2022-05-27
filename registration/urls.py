from django.urls import path

from . import views

urlpatterns = [
    path("Registration", views.registrationRequest, name='Registration'),
    path("myApplications", views.myApplications, name='applications'),
    path("registrationRenewal", views.registrationRenewal, name='renewal'),
]