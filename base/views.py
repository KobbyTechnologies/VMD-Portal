from django.contrib import messages
from django.shortcuts import render

# Create your views here.
def sidebar(request):
    return render(request, "sidebar.html")
def profileRequest(request):
    if request.method == "POST":
        try:
            fullName = request.POST.get('fullName')
            manufacturer = request.POST.get('manufacturer')
            about = request.POST.get('about')
            country = request.POST.get('country')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
        except ValueError:
            pass 
    return render(request,'profile.html')
def contact(request):
    return render(request,'contact.html')

def FAQRequest(request):
    return render(request,'faq.html')