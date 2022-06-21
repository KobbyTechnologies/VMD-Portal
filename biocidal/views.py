from django.shortcuts import render,redirect
from django.conf import settings as config
from django.contrib import messages
import requests

# Create your views here.
def biocidalRegistration(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = 'modify'
            prodName = request.POST.get('prodName')
            otherNames = request.POST.get('otherNames')
            chemicalName = request.POST.get('chemicalName')
            casNumber = request.POST.get('casNumber')
            intendedUse = request.POST.get('intendedUse')
            instructions = request.POST.get('instructions')
            proposedShelfLife =request.POST.get('proposedShelfLife')
            shelfLifeAfterFirstOpening =request.POST.get('shelfLifeAfterFirstOpening')
            ShelfLifeAfterDilution = request.POST.get('ShelfLifeAfterDilution')
            visualDescription = request.POST.get('visualDescription')
            packagingMaterial = request.POST.get('packagingMaterial')
            closureSystem = request.POST.get('closureSystem')
            packSize = request.POST.get('packSize')

            iAgree = eval(request.POST.get('iAgree'))
            userId = request.session['UserID']
            if not iAgree:
                iAgree = False         
            
            try:
                response = config.CLIENT.service.BiocidalCard(prodNo,myAction,prodName,otherNames,
                chemicalName,casNumber,intendedUse,instructions,proposedShelfLife,
                shelfLifeAfterFirstOpening,ShelfLifeAfterDilution,visualDescription,packagingMaterial,
                packSize,closureSystem,userId,iAgree)
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