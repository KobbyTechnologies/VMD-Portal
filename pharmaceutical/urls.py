from django.urls import path

from . import views

urlpatterns = [
    path("VeterinaryPharmaceutical", views.VeterinaryPharmaceutical, name='VeterinaryPharmaceutical'),
    path("pharmDetails",views.pharmDetails,name='pharmDetails'),
]