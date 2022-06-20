from django.shortcuts import render

# Create your views here.
def PaymentGateway(request,pk):
    return render(request,'gateway.html')