from django.shortcuts import render,redirect
from django.conf import settings as config
from django.contrib import messages
import requests

# Create your views here.
def feedRegistration(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = 'modify'
            prodName = request.POST.get('prodName')
            proposedCategory = request.POST.get('proposedCategory')
            casNumber = request.POST.get('casNumber')
            otherNames = request.POST.get('otherNames')
            intendedUse = request.POST.get('intendedUse')
            dosageForm = request.POST.get('dosageForm')
            dosage =request.POST.get('dosage')
            proposedShelfLife =request.POST.get('proposedShelfLife')
            shelfLifeAfterFirstOpening =request.POST.get('shelfLifeAfterFirstOpening')
            ShelfLifeAfterDilution = request.POST.get('ShelfLifeAfterDilution')
            countryOfOrigin = request.POST.get('countryOfOrigin')
            visualDescription = request.POST.get('visualDescription')
            packagingMaterial = request.POST.get('packagingMaterial')
            closureSystem = request.POST.get('closureSystem')
            packSize = request.POST.get('packSize')
            iAgree = eval(request.POST.get('iAgree'))
            userId = request.session['UserID']
            if not iAgree:
                iAgree = False         
            
            try:
                response = config.CLIENT.service.FeedAdditivesCard(prodNo,myAction,prodName,proposedCategory,casNumber,
                otherNames,intendedUse,dosage,packSize,dosageForm,proposedShelfLife,ShelfLifeAfterDilution,
                countryOfOrigin,visualDescription,packagingMaterial,closureSystem,shelfLifeAfterFirstOpening,
                userId,iAgree)
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

def Additive (request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            AdditiveName = request.POST.get('AdditiveName')
            Proportion = request.POST.get('Proportion')
            specification = request.POST.get('specification')
            userId = request.session['UserID']
            try:
                response = config.CLIENT.service.Addictives(prodNo,myAction,AdditiveName,Proportion,specification,userId)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully.")
                    return redirect('productDetails',pk=pk)
                else:
                    print("Not sent")
                    return redirect ('productDetails',pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('productDetails', pk=prodNo)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect ('productDetails',pk=pk)