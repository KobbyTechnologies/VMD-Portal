from django.urls import path

from . import views

urlpatterns = [
    path("feed/additives/<str:pk>", views.feedRegistration, name='feedRegistration'),
    path("additives/<str:pk>", views.Additive, name='Additive'),
]