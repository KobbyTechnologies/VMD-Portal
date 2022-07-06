from django.urls import path

from . import views

urlpatterns = [
    path("appeal/request", views.appealRequest, name='appeal'),
    path("ApplyAppeal/<str:pk>/<str:id>",views.ApplyAppeal,name='ApplyAppeal'),
    path("appealDetails/<str:pk>",views.appealDetails,name='appealDetails'),
    path("appealGateway/<str:pk>",views.appealGateway,name='appealGateway'),
]