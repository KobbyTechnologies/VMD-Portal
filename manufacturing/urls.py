from django.urls import path

from . import views

urlpatterns = [
    path(
        "ManufacturingLicense/",
        views.ManufacturingLicense.as_view(),
        name="ManufacturingLicense",
    ),
    path(
        "ManufacturingLicense/<str:pk>/",
        views.ManufacturingLicenseDetails.as_view(),
        name="ManufacturingLicenseDetails",
    ),
    path(
        "ManufacturingLicenseLines/<str:pk>/",
        views.ManufacturingLicenseLines.as_view(),
        name="ManufacturingLicenseLines",
    ),
    path(
        "ManufacturingLicenseCustomer/",
        views.ManufacturingLicenseCustomer.as_view(),
        name="ManufacturingLicenseCustomer",
    ),
    path(
        "ManufacturingLicenseInvoice/",
        views.ManufacturingLicenseInvoice.as_view(),
        name="ManufacturingLicenseInvoice",
    ),
    path(
        "ManufacturingLicenseAttachments/<str:pk>/",
        views.ManufacturingLicenseAttachments.as_view(),
        name="ManufacturingLicenseAttachments",
    ),
    path(
        "submit/manufacturing/license/<str:pk>/",
        views.SubmitManufacturingLicense.as_view(),
        name="SubmitManufacturingLicense",
    ),
    path(
        "manufacturing/license/cert/<str:pk>/",
        views.ManufacturingLicenseCert.as_view(),
        name="ManufacturingLicenseCert",
    ),
]
