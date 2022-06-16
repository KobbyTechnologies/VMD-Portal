from django.contrib import messages
from django.shortcuts import render,redirect
from django.conf import settings as config
import requests 

# Create your views here.
def vaccineRegistration(request):
    if request.method == 'POST':
        try:
            prodNo = request.POST.get('prodNo')
            myAction = request.POST.get('myAction')
            prodName = request.POST.get('prodName')
            packSize = request.POST.get('packSize')
            description = request.POST.get('description')
            mainIndication = request.POST.get('mainIndication')
            TypeOfReview = request.POST.get('TypeOfReview')
            giveReasons = request.POST.get('giveReasons')
            iAgree = eval(request.POST.get('iAgree'))
            nameOfSignatory = request.POST.get('nameOfSignatory')
            userId = request.session['UserID']
            if not iAgree:
                iAgree = False
            if not giveReasons:
                giveReasons = ''
            try:
                response = config.CLIENT.service.FnVaccineCard(prodNo,myAction,prodName,packSize,
                description,mainIndication,TypeOfReview,giveReasons,iAgree,nameOfSignatory,userId)
                print(response)
                if response == True:
                    return redirect('applications', pk=prodNo)
                else:
                    print('not sent')
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('applications', pk=prodNo)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
        return redirect('login')
    return redirect('applications', pk=prodNo)