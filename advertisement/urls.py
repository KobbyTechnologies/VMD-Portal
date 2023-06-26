from django.urls import path

from . import views

urlpatterns = [
    path("advertise/", views.Advertisement.as_view(), name="advertise"),
    path(
        "advertise/<str:pk>/", views.AdvertiseDetails.as_view(), name="AdvertiseDetails"
    ),
    path(
        "AdvertisementLines/<str:pk>/",
        views.AdvertisementLines.as_view(),
        name="AdvertisementLines",
    ),
    path(
        "AdvertisingCustomer/",
        views.AdvertisingCustomer.as_view(),
        name="AdvertisingCustomer",
    ),
    path(
        "AdvertisingInvoice/",
        views.AdvertisingInvoice.as_view(),
        name="AdvertisingInvoice",
    ),
    path(
        "AdvertAttachments/<str:pk>/",
        views.AdvertAttachments.as_view(),
        name="AdvertAttachments",
    ),
    path(
        "submit/advert/<str:pk>/",
        views.SubmitAdvert.as_view(),
        name="SubmitAdvert",
    ),
    path(
        "premise/cert/<str:pk>/",
        views.AdvertCert.as_view(),
        name="AdvertCert",
    ),
]
