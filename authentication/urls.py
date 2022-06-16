from django.urls import path
from . import views

urlpatterns = [
    path("Register", views.registerRequest,name='register'),
    path("registerAccount", views.registerAccount,name='registerAccount'),
    path("", views.loginRequest,name='login'),
    path("verify", views.verifyRequest,name='verify'),
    path("reset", views.reset_request,name='reset'),
    path("resetPassword", views.resetPassword,name='resetPassword'),
    path("logout", views.logout_request,name='logout'),
]