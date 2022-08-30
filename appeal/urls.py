from django.urls import path

from . import views

urlpatterns = [
    path("appeal/request", views.appealRequest.as_view(), name='appeal'),
    path("appealDetails/<str:pk>",views.appealDetails.as_view(),name='appealDetails'),
    path("appealGateway/<str:pk>",views.appealGateway.as_view(),name='appealGateway'),
]