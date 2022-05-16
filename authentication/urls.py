from django.urls import path
from . import views

urlpatterns = [
    path("Register", views.registerRequest,name='register'),
    path("", views.loginRequest,name='login'),
]