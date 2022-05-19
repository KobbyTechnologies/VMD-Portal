from django.shortcuts import render

# Create your views here.
def sidebar(request):
    return render(request, "sidebar.html")
def profileRequest(request):
    return render(request,'profile.html')
def contact(request):
    return render(request,'contact.html')