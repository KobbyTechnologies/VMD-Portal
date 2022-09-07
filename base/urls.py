from django.urls import path
from . import views

urlpatterns = [
    path("sidebar", views.sidebar,name='sidebar'),
    path("profile", views.profileRequest,name='profile'),
    path("contact", views.contact,name='contact'),
    path("faq", views.FAQRequest,name='faq'),
    path("Manual", views.Manual,name='Manual'),
]