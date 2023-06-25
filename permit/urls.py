from django.urls import path

from . import views

urlpatterns = [
    path("permit/", views.Permit.as_view(), name="permit"),
    path("permit/<str:pk>/", views.PermitDetails.as_view(), name="PermitDetails"),
    path(
        "Professionals/<str:pk>/", views.Professionals.as_view(), name="Professionals"
    ),
    path("customer/", views.Customer.as_view(), name="customer"),
    path("invoice/", views.FNGenerateInvoice.as_view(), name="invoice"),
    path(
        "PermitAttachments/<str:pk>/",
        views.PermitAttachments.as_view(),
        name="PermitAttachments",
    ),
    path(
        "RemovePermitAttachment/",
        views.RemovePermitAttachment.as_view(),
        name="RemovePermitAttachment",
    ),
    path(
        "submit/permit/<str:pk>/",
        views.SubmitWholesalePermit.as_view(),
        name="submitPermit",
    ),
    path(
        "premise/cert/<str:pk>/",
        views.PremiseCert.as_view(),
        name="PremiseCert",
    ),
]
