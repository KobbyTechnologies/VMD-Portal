from django.urls import path
from . import views

urlpatterns = [
    path("Register", views.registerRequest,name='register'),
    path("registerAccount", views.registerAccount,name='registerAccount'),
    path("", views.loginRequest,name='login'),
    path("verify", views.verifyRequest,name='verify'),
]