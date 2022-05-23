from django.shortcuts import render

# Create your views here.
def vaccineRegistration(request):
    return render(request,'vaccine.html')