from django.urls import path

from . import views

urlpatterns = [
    path("Disposal/", views.Disposal.as_view(), name="Disposal"),
    path("Disposal/<str:pk>/", views.DisposalDetails.as_view(), name="DisposalDetails"),
    path(
        "DisposalLines/<str:pk>/", views.DisposalLines.as_view(), name="DisposalLines"
    ),
    path(
        "DisposalCustomer/", views.DisposalCustomer.as_view(), name="DisposalCustomer"
    ),
    path("DisposalInvoice/", views.DisposalInvoice.as_view(), name="DisposalInvoice"),
    path(
        "DisposalAttachments/<str:pk>/",
        views.DisposalAttachments.as_view(),
        name="DisposalAttachments",
    ),
    path(
        "submit/disposal/<str:pk>/",
        views.DisposalPharmacy.as_view(),
        name="DisposalPharmacy",
    ),
    path(
        "disposal/cert/<str:pk>/",
        views.DisposalCert.as_view(),
        name="DisposalCert",
    ),
    path(
        "TechnicalRequirements/<str:pk>/",
        views.TechnicalRequirements.as_view(),
        name="TechnicalRequirements",
    ),
]
