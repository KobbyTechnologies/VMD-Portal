from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("Registration", views.registrationRequest, name='Registration'),
]