from django.shortcuts import render

# Create your views here.
def sidebar(request):
    return render(request, "sidebar.html")