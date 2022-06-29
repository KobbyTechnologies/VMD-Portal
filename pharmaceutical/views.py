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
            visualDescription = request.POST.get('visualDescription')
            PharmaceuticalDosage = request.POST.get('PharmaceuticalDosage')
            RouteOfAdministration = request.POST.get('RouteOfAdministration')
            shelfLifeAfterDilution = request.POST.get('shelfLifeAfterDilution')
            shelfLifeAfterFirstOpening =request.POST.get('shelfLifeAfterFirstOpening')
            storageConditions =request.POST.get('storageConditions')
            storageAfterOpening =request.POST.get('storageAfterOpening')
            PharmacotherapeuticGroup = request.POST.get('PharmacotherapeuticGroup')
            AssignedATCCode =  eval(request.POST.get('AssignedATCCode'))
            ATCCode = request.POST.get('ATCCode')
            AppliedATCCode = request.POST.get('AppliedATCCode')
            SubjectMedicalPrescription = request.POST.get('SubjectMedicalPrescription')
            controlledVeterinaryMedicine = request.POST.get('controlledVeterinaryMedicine')
            prescriptionOnlyMedicine = request.POST.get('prescriptionOnlyMedicine')
            nonPharmacy = request.POST.get('nonPharmacy')
            pharmaciesOnly = request.POST.get('pharmaciesOnly')
            iAgree = eval(request.POST.get('iAgree'))
            userId = request.session['UserID']
            if not iAgree:
                iAgree = False
            if not ATCCode:
                ATCCode = ''
            if not AppliedATCCode:
                AppliedATCCode = 'True'
            if not controlledVeterinaryMedicine:
                controlledVeterinaryMedicine = 'False'
            if not prescriptionOnlyMedicine:
                prescriptionOnlyMedicine = 'False'
            if not nonPharmacy:
                nonPharmacy = 'False'
            if not pharmaciesOnly:
                pharmaciesOnly = 'False'

            AppliedATCCode = eval(AppliedATCCode)
            print("Atc",AppliedATCCode)
            nonPharmacy = eval(nonPharmacy)
            pharmaciesOnly = eval(pharmaciesOnly)
            SubjectMedicalPrescription = eval(SubjectMedicalPrescription)
            controlledVeterinaryMedicine = eval(controlledVeterinaryMedicine)
            
            try:
                response = config.CLIENT.service.FnPharmaceuticalCard(pk,myAction,prodName,packSize,visualDescription,
                PharmaceuticalDosage,RouteOfAdministration,shelfLifeAfterDilution,shelfLifeAfterFirstOpening,
                storageConditions,storageAfterOpening,PharmacotherapeuticGroup,AssignedATCCode
                ,ATCCode,AppliedATCCode,SubjectMedicalPrescription,controlledVeterinaryMedicine,
                prescriptionOnlyMedicine,nonPharmacy,pharmaciesOnly,
                userId,iAgree
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


