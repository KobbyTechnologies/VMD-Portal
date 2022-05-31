from django.shortcuts import render

# Create your views here.
def replacementRequest(request):
    return render(request,"replacement.html")