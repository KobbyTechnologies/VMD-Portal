from django.urls import path

from . import views

urlpatterns = [
    path("VeterinaryPharmaceutical", views.VeterinaryPharmaceutical, name='VeterinaryPharmaceutical'),
]