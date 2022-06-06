from django.shortcuts import render

# Create your views here.
def VeterinaryPharmaceutical(request):
    return render(request,'pharmaceutical.html')

def pharmDetails (request):
    return render(request,"pharmDetails.html")