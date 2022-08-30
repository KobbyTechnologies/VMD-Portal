from django.shortcuts import render,redirect
from django.conf import settings as config
from django.contrib import messages
import requests

# Create your views here.
def VeterinaryPharmaceutical(request,pk):
    if request.method == 'POST':
        try:
            myAction = 'modify'
            prodName = request.POST.get('prodName')
            packSize = request.POST.get('packSize')
            PharmaceuticalDosage = request.POST.get('PharmaceuticalDosage')
            RouteOfAdministration = request.POST.get('RouteOfAdministration')
            shelfLifeAfterDilution = request.POST.get('shelfLifeAfterDilution')
            shelfLifeAfterFirstOpening =request.POST.get('shelfLifeAfterFirstOpening')
            storageConditions =request.POST.get('storageConditions')
            storageAfterOpening =request.POST.get('storageAfterOpening')
            PharmacotherapeuticGroup = request.POST.get('PharmacotherapeuticGroup')
            ATCCode = request.POST.get('ATCCode')
            controlledVeterinaryMedicine = request.POST.get('controlledVeterinaryMedicine')
            prescriptionOnlyMedicine = request.POST.get('prescriptionOnlyMedicine')
            nonPharmacy = request.POST.get('nonPharmacy')
            pharmaciesOnly = request.POST.get('pharmaciesOnly')
            iAgree = eval(request.POST.get('iAgree'))
            userId = request.session['UserID']
            CountryOfOrigin = request.POST.get('CountryOfOrigin')
            CountryOfRelease = request.POST.get('CountryOfRelease')
            if not iAgree:
                iAgree = False
            if not controlledVeterinaryMedicine:
                controlledVeterinaryMedicine = 'False'
            if not prescriptionOnlyMedicine:
                prescriptionOnlyMedicine = 'False'
            if not nonPharmacy:
                nonPharmacy = 'False'
            if not pharmaciesOnly:
                pharmaciesOnly = 'False'
            if not ATCCode:
                messages.info(request,"You must have an ATC Code to register a product")
                return redirect('registration')

            nonPharmacy = eval(nonPharmacy)
            pharmaciesOnly = eval(pharmaciesOnly)
            controlledVeterinaryMedicine = eval(controlledVeterinaryMedicine)
            
            try:
                response = config.CLIENT.service.FnPharmaceuticalCard(pk,myAction,prodName,packSize,
                PharmaceuticalDosage,RouteOfAdministration,shelfLifeAfterDilution,shelfLifeAfterFirstOpening,
                storageConditions,storageAfterOpening,PharmacotherapeuticGroup
                ,ATCCode,controlledVeterinaryMedicine,
                prescriptionOnlyMedicine,nonPharmacy,pharmaciesOnly,userId,CountryOfOrigin,CountryOfRelease,
                iAgree
                )
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


