from django.shortcuts import render

# Create your views here.

def registrationRequest(request):
    return render(request,'registration.html')