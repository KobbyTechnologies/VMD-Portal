from django.shortcuts import render

# Create your views here.
def feedRegistration(request):
    return render(request,"feed.html")