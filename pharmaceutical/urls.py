from django.urls import path

from . import views

urlpatterns = [
    path(
        "VeterinaryPharmaceutical/<str:pk>",
        views.VeterinaryPharmaceutical.as_view(),
        name="VeterinaryPharmaceutical",
    ),
]
