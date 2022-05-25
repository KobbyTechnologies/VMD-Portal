from django.shortcuts import render

# Create your views here.
def variation(request):
    return render(request,"variation.html")