from django.urls import path

from . import views

urlpatterns = [
    path("feedRegistration", views.feedRegistration, name='feedRegistration'),
]