from django.urls import path

from . import views

urlpatterns = [
    path("VeterinaryPharmaceutical/<str:pk>", views.VeterinaryPharmaceutical, name='VeterinaryPharmaceutical'),
]