from django.urls import path

from . import views

urlpatterns = [
    path("appeal/request", views.appealRequest, name='appeal'),
    path("ApplyAppeal/<str:pk>",views.ApplyAppeal,name='ApplyAppeal'),
]