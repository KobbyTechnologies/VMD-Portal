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
    # path("customer/", views.Customer.as_view(), name="customer"),
    # path("invoice/", views.FNGenerateInvoice.as_view(), name="invoice"),
    # path(
    #     "PermitAttachments/<str:pk>/",
    #     views.PermitAttachments.as_view(),
    #     name="PermitAttachments",
    # ),
    # path(
    #     "RemovePermitAttachment/",
    #     views.RemovePermitAttachment.as_view(),
    #     name="RemovePermitAttachment",
    # ),
    # path(
    #     "submit/permit/<str:pk>/",
    #     views.SubmitWholesalePermit.as_view(),
    #     name="submitPermit",
    # ),
    # path(
    #     "premise/cert/<str:pk>/",
    #     views.PremiseCert.as_view(),
    #     name="PremiseCert",
    # ),
]
