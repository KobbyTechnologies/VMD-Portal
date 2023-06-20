from django.urls import path

from . import views

urlpatterns = [
    path(
        "product/registration", views.registrationRequest.as_view(), name="Registration"
    ),
    path(
        "product/application/<str:pk>",
        views.myApplications.as_view(),
        name="applications",
    ),
    path("productClass", views.ProductClass.as_view(), name="productClass"),
    path(
        "manufacturer/particulars/<str:pk>",
        views.ManufacturesParticulars.as_view(),
        name="ManufacturesParticulars",
    ),
    path(
        "product/details/<str:pk>",
        views.productDetails.as_view(),
        name="productDetails",
    ),
    path(
        "active/ingredients/<str:pk>", views.Ingredients.as_view(), name="Ingredients"
    ),
    path(
        "country/registered/<str:pk>",
        views.CountryRegistered.as_view(),
        name="CountryRegistered",
    ),
    path(
        "marketing/authorization/<str:pk>",
        views.MarketingAuthorization.as_view(),
        name="MarketingAuthorization",
    ),
    path("makePayment/<str:pk>", views.makePayment.as_view(), name="makePayment"),
    path("submit/<str:pk>", views.SubmitRegistration, name="SubmitRegistration"),
    path("Attachments/<str:pk>/", views.Attachments.as_view(), name="Attachments"),
    path(
        "GenerateCertificate/<str:pk>",
        views.GenerateCertificate,
        name="GenerateCertificate",
    ),
    path(
        "DeleteAttachment/", views.DeleteAttachment.as_view(), name="DeleteAttachment"
    ),
    path("FnRegulatory/<str:pk>", views.FnRegulatory, name="FnRegulatory"),
    path("filter_list/<str:pk>", views.filter_list.as_view(), name="filter_list"),
]
