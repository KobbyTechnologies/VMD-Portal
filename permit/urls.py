from django.urls import path

from . import views

urlpatterns = [
    path("permit/", views.Permit.as_view(), name="permit"),
    path("permit/<str:pk>/", views.PermitDetails.as_view(), name="PermitDetails"),
    path(
        "Professionals/<str:pk>/", views.Professionals.as_view(), name="Professionals"
    ),
]
