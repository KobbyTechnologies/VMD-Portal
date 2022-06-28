from django.urls import path

from . import views

urlpatterns = [
    path("retention", views.registrationRetention, name='retention'),
    path("ApplyRetention/<str:pk>",views.ApplyRetention,name='ApplyRetention'),
]