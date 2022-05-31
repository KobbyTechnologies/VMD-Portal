from django.urls import path

from . import views

urlpatterns = [
    path("replacementRequest", views.replacementRequest, name='replacement'),
]