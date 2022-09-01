from django.shortcuts import render,redirect
from django.conf import settings as config
from django.contrib import messages
import requests
from datetime import date, datetime

# Create your views here.
def pesticideRegistration(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = 'modify'
            prodName = request.POST.get('prodName')
            packSize = request.POST.get('packSize')
            proposedShelfLife = request.POST.get('proposedShelfLife')
            storageConditions = request.POST.get('storageConditions')
            shelfLifeAfterFirstOpening = request.POST.get('shelfLifeAfterFirstOpening')
            storageAfterOpening =request.POST.get('storageAfterOpening')
            tradeMark = request.POST.get('tradeMark')
            formulation = request.POST.get('formulation')
            othersIndicate = request.POST.get('othersIndicate')
            visualDescription = request.POST.get('visualDescription')
            targetAnimals = request.POST.get('targetAnimals')
            targetParasites = request.POST.get('targetParasites')
            frequencyApplication = int(request.POST.get('frequencyApplication'))    
            animalSafety = request.POST.get('animalSafety')
            withholdingPeriod =  request.POST.get('withholdingPeriod')
            maximumLimit = request.POST.get('maximumLimit')
            iAgree = eval(request.POST.get('iAgree'))
            userId = request.session['UserID']
            signatoryName = request.POST.get('signatoryName')
            signatoryPosition = request.POST.get('signatoryPosition')
            companyName = request.POST.get('companyName')
            companyAddress = request.POST.get('companyAddress')
            CountryOrigin = request.POST.get('CountryOrigin')
            companyTel = request.POST.get('companyTel')
            companyFax = request.POST.get('companyFax')
            companyEmail = request.POST.get('companyEmail')
            if not iAgree:
                iAgree = False                   

            try:
                
                response = config.CLIENT.service.PesticideCard(prodNo,myAction,prodName,packSize,proposedShelfLife,
                storageConditions,shelfLifeAfterFirstOpening,storageAfterOpening,tradeMark,othersIndicate,
                visualDescription,targetAnimals,targetParasites,frequencyApplication,animalSafety,withholdingPeriod,maximumLimit,
                formulation,userId,iAgree,signatoryName,signatoryPosition,companyName,companyAddress,CountryOrigin,
                companyTel,companyFax,companyEmail)

                print(response)
                if response == True:
                    messages.success(request,"Successfully Saved")
                    return redirect('productDetails', pk=pk)
                else:
                    messages.success(request,"Not sent. Retry Again")
                    return redirect('applications', pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('applications', pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        except ValueError as e:
            messages.info(request,"Invalid Input")
            print(e)
            return redirect('applications', pk=pk)
    return redirect('applications', pk=pk)