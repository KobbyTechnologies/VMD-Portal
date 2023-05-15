from django.shortcuts import render,redirect
from django.conf import settings as config
from django.contrib import messages
import requests

# Create your views here.
def devicesRegistration(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = 'modify'
            Classification = request.POST.get('Classification')
            prodName = request.POST.get('prodName')
            DeviceOverview = request.POST.get('DeviceOverview')
            marketingHistory = request.POST.get('marketingHistory')
            intendedUse = request.POST.get('intendedUse')
            ImportantSafety = request.POST.get('ImportantSafety')
            visualDescription =request.POST.get('visualDescription')
            instructions =request.POST.get('instructions')
            diseaseDescription =request.POST.get('diseaseDescription')
            hazardAlert = request.POST.get('hazardAlert')
            specialCare = request.POST.get('Care')
            Characterization = request.POST.get('Characterization')
            Functional = request.POST.get('Functional')
            LabelsOnDevice = request.POST.get('LabelsOnDevice')
            DevicePackaging = request.POST.get('DevicePackaging')
            Manual = request.POST.get('Manual')
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
            if not Manual:
                Manual = 'False'
            Manual = eval(Manual)
            try:
                response = config.CLIENT.service.DevicesCard(prodNo,myAction,prodName,Classification,
                DeviceOverview,marketingHistory,intendedUse,ImportantSafety,visualDescription,instructions,
                diseaseDescription,hazardAlert,specialCare,Characterization,Functional,LabelsOnDevice,
                DevicePackaging,Manual,userId,iAgree,signatoryName,signatoryPosition,companyName,
                companyAddress,CountryOrigin,companyTel,companyFax,companyEmail)
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

def essentialPrinciples(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            lineNo = request.POST.get('lineNo')
            generalMethod = request.POST.get('generalMethod')
            generalMethod = request.POST.get('essentialPrinciple')
            userId = request.session['UserID']
            
            try:
                response = config.CLIENT.service.UsedMethods(prodNo,myAction,generalMethod,generalMethod,userId,lineNo)
                print(response)
                if response == True:
                    messages.success(request,"Request Successful")
                    return redirect('productDetails',pk=pk)
                else:
                    print("Not sent")
                    return redirect ('productDetails',pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('productDetails', pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect ('productDetails',pk=pk)