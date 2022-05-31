from django.shortcuts import render

# Create your views here.
def appealRequest(request):
    return render(request,'appeal.html')