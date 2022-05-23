from django.urls import path

from . import views

urlpatterns = [
    path("vaccineRegistration", views.vaccineRegistration, name='vaccineRegistration'),
]