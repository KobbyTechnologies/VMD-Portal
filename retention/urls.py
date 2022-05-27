from django.urls import path

from . import views

urlpatterns = [
    path("retention", views.retention, name='retention'),
]