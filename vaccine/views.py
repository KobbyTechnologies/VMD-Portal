from django.contrib import messages
from django.shortcuts import render,redirect
from django.conf import settings as config
import requests 

# Create your views here.
def vaccineRegistration(request,pk):
    if request.method == 'POST':
        try:
            myAction = 'modify'
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
                response = config.CLIENT.service.FnVaccineCard(pk,myAction,prodName,packSize,
                description,mainIndication,TypeOfReview,giveReasons,iAgree,nameOfSignatory,userId)
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

