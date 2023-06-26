from django.urls import path

from . import views

urlpatterns = [
    path("retailer/permit/", views.RetailersPermit.as_view(), name="RetailersPermit"),
    path(
        "retailer/<str:pk>/",
        views.RetailerPermitDetails.as_view(),
        name="RetailerPermitDetails",
    ),
    path(
        "RetailProfessionals/<str:pk>/",
        views.RetailProfessionals.as_view(),
        name="RetailProfessionals",
    ),
    path("RetailCustomer/", views.RetailCustomer.as_view(), name="RetailCustomer"),
    path("RetailerInvoice/", views.RetailerInvoice.as_view(), name="RetailerInvoice"),
    path(
        "RetailPermitAttachments/<str:pk>/",
        views.RetailPermitAttachments.as_view(),
        name="RetailPermitAttachments",
    ),
    path(
        "RemoveRetailAttachment/",
        views.RemoveRetailAttachment.as_view(),
        name="RemoveRetailAttachment",
    ),
    path(
        "submit/retail/<str:pk>/",
        views.SubmitRetailPermit.as_view(),
        name="SubmitRetailPermit",
    ),
    path(
        "retail/cert/<str:pk>/",
        views.RetailPremiseCert.as_view(),
        name="RetailPremiseCert",
    ),
]
