from django.shortcuts import redirect, render
from django.conf import settings as config
import requests 
from django.contrib import messages

# Create your views here.

def registrationRequest(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYVertinaryclasses")
    try:
        response = session.get(Access_Point, timeout=10).json()
        product = response['value']
    except requests.exceptions.ConnectionError as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    ctx = {"product": product}
    return render(request,'registration.html',ctx)

def myApplications(request):
    return render(request, "applications.html")

def registrationRenewal(request):
    return render(request,"renewal.html")