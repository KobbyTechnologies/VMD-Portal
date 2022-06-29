from django.urls import path
from . import views

urlpatterns = [
    path('GMP', views.GMPApplication, name='gmp'),
     path('ApplyGMP', views.ApplyGMP, name='ApplyGMP'),
    path('GMPDetails/<str:pk>', views.GMPDetails, name='GMPDetails'),
    path('linesToInspect/<str:pk>', views.linesToInspect, name='linesToInspect'),
]