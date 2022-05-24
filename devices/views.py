from urllib import request
from django.shortcuts import render

# Create your views here.
def devicesRegistration(request):
    return render(request,"devices.html")