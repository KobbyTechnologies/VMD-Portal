from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("base.urls")),
    path("", include("dashboard.urls")),
    path("", include("registration.urls")),
    path("", include("pharmaceutical.urls")),
    path("", include("vaccine.urls")),
    path("", include("pesticide.urls")),
    path("", include("feed.urls")),
    path("", include("biocidal.urls")),
    path("", include("devices.urls")),
    path("", include("variation.urls")),
    path("", include("appeal.urls")),
    path("", include("payment.urls")),
    path("", include("retention.urls")),
    path("", include("renewal.urls")),
    path("", include("gmp.urls")),
    path("", include("permit.urls")),
    path("", include("retailers.urls")),
    path("", include("advertisement.urls")),
    path("", include("pharmacy_permit.urls")),
    path("", include("disposal.urls")),
    path("", include("manufacturing.urls")),
]
