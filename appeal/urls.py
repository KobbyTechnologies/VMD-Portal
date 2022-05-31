from django.urls import path

from . import views

urlpatterns = [
    path("appealRequest", views.appealRequest, name='appeal'),
]