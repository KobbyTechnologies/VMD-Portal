from django.urls import path

from . import views

urlpatterns = [
    path("vaccineRegistration/<str:pk>", views.vaccineRegistration, name='vaccineRegistration'),
]