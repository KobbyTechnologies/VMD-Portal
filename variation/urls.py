from django.urls import path

from . import views

urlpatterns = [
    path("variation", views.variation, name='variation'),
    path("ApplyVariation/<str:pk>",views.ApplyVariation,name='ApplyVariation'),
]