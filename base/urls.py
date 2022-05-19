from django.urls import path
from . import views

urlpatterns = [
    path("sidebar", views.sidebar,name='sidebar'),
    path("profile", views.profileRequest,name='profile'),
]