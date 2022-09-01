from django.contrib import messages
from django.shortcuts import render,redirect
from django.conf import settings as config
import json
import requests 

# Create your views here.
def vaccineRegistration(request,pk):
    if request.method == 'POST':
        try:
            myAction = 'modify'
            prodName = request.POST.get('prodName')
            packSize = request.POST.get('packSize')
            mainIndication = request.POST.get('mainIndication')
            TypeOfReview = request.POST.get('TypeOfReview')
            giveReasons = request.POST.get('giveReasons')
            iAgree = eval(request.POST.get('iAgree'))
            userId = request.session['UserID']
            DosageForm = request.POST.get('DosageForm')
            description = request.POST.get('description')
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
            if not giveReasons:
                giveReasons = ''
            try:
                response = config.CLIENT.service.FnVaccineCard(pk,myAction,prodName,packSize,
                mainIndication,TypeOfReview,giveReasons,description,DosageForm,iAgree,userId,signatoryName,
                signatoryPosition,companyName,companyAddress,CountryOrigin,companyTel,companyFax,companyEmail)
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
        except TypeError as e:
            print(e)
            return redirect('applications', pk=pk)
    return redirect('applications', pk=pk)

