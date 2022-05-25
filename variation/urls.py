from django.urls import path

from . import views

urlpatterns = [
    path("variation", views.variation, name='variation'),
]