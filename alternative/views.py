from django.shortcuts import render

# Create your views here.
def alternativeRegistration(request):
    return render(request,"alternative.html")