from django.urls import path

from . import views

urlpatterns = [
    path(
        "pharmacy/",
        views.PremisePermitForVeterinaryPharmacy.as_view(),
        name="VeterinaryPharmacy",
    ),
    path("pharmacy/<str:pk>/", views.PharmacyDetails.as_view(), name="PharmacyDetails"),
    path(
        "PharmacyProfessionals/<str:pk>/",
        views.PharmacyProfessionals.as_view(),
        name="PharmacyProfessionals",
    ),
    path(
        "PharmacyCustomer/",
        views.PharmacyCustomer.as_view(),
        name="PharmacyCustomer",
    ),
    path(
        "PharmacyInvoice/",
        views.PharmacyInvoice.as_view(),
        name="PharmacyInvoice",
    ),
    path(
        "PharmacyAttachments/<str:pk>/",
        views.PharmacyAttachments.as_view(),
        name="PharmacyAttachments",
    ),
    path(
        "submit/pharmacy/<str:pk>/",
        views.SubmitPharmacy.as_view(),
        name="SubmitPharmacy",
    ),
    path(
        "pharmacy/cert/<str:pk>/",
        views.PharmacyCert.as_view(),
        name="PharmacyCert",
    ),
]
