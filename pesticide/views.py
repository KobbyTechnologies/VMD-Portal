from ast import Return
from django.shortcuts import render

# Create your views here.
def pesticideRegistration(request):
    return render(request,'pesticide.html')