from django.urls import path
from . import views

urlpatterns = [
    path('GMP', views.GMPApplication, name='gmp'),
    path('GMPDetails', views.GMPDetails, name='GMPDetails'),
]