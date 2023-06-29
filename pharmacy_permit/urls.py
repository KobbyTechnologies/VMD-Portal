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
    # path(
    #     "AdvertisingInvoice/",
    #     views.AdvertisingInvoice.as_view(),
    #     name="AdvertisingInvoice",
    # ),
    # path(
    #     "AdvertAttachments/<str:pk>/",
    #     views.AdvertAttachments.as_view(),
    #     name="AdvertAttachments",
    # ),
    # path(
    #     "submit/advert/<str:pk>/",
    #     views.SubmitAdvert.as_view(),
    #     name="SubmitAdvert",
    # ),
    # path(
    #     "advert/cert/<str:pk>/",
    #     views.AdvertCert.as_view(),
    #     name="AdvertCert",
    # ),
]
