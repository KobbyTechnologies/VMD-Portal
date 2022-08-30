from django.urls import path

from . import views

urlpatterns = [
    path("appeal/request", views.appealRequest.as_view(), name='appeal'),
    path("appealDetails/<str:pk>",views.appealDetails,name='appealDetails'),
    path("appealGateway/<str:pk>",views.appealGateway,name='appealGateway'),
    path("SubmitAppeal/<str:pk>",views.SubmitAppeal,name='SubmitAppeal'),
]