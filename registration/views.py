from django.shortcuts import render

# Create your views here.

def registrationRequest(request):
    return render(request,'registration.html')

def myApplications(request):
    return render(request, "applications.html")

def registrationRenewal(request):
    return render(request,"renewal.html")