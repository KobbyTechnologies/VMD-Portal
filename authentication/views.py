from django.shortcuts import render


# Register View
def registerRequest(request):
    return render(request,"register.html")

# Login View
def loginRequest(request):
    return render(request,"login.html")