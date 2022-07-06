from django.shortcuts import render,redirect
import requests
import json
from django.conf import settings as config
from django.contrib import messages
from datetime import date, datetime

# Create your views here.
def variation(request):
    session = requests.Session()
    session.auth = config.AUTHS
    variation= config.O_DATA.format("/QYVariation")

    OpenProducts = []
    Pending = []
    Approved = []
    Rejected =[]
    try:
        response = session.get(variation, timeout=10).json()

        for res in response['value']:
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Open':
                output_json = json.dumps(res)
                OpenProducts.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Pending Approval':
                output_json = json.dumps(res)
                Pending.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Approved':
                output_json = json.dumps(res)
                Approved.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Rejected':
                output_json = json.dumps(res)
                Rejected.append(json.loads(output_json))

    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    openCount = len(OpenProducts)
    pendCount = len(Pending)
    appCount = len(Approved)
    rejectedCount = len(Rejected)
    ctx = {"openCount":openCount,"open":OpenProducts,
    "pendCount":pendCount,"pending":Pending,"appCount":appCount,"approved":Approved,
    "rejectedCount":rejectedCount,"rejected":Rejected}
    return render(request,"variation.html",ctx)

def ApplyVariation(request,pk,id):
    if request.method == 'POST':
        try:
            myAction = 'modify'
            dosageForms = request.POST.get('dosageForms')
            typeofChange = request.POST.get('typeofChange')
            otherApplications = request.POST.get('otherApplications')
            scope = request.POST.get('scope')
            background = request.POST.get('background')
            present = request.POST.get('background')
            proposed = request.POST.get('proposed')


            response = config.CLIENT.service.FnVariation(pk,myAction,request.session['UserID'],dosageForms,id,
            typeofChange,otherApplications,scope,background,present,proposed)
            print(response)
            if response == True:
                messages.success(request,"Saved Successfully")
                return redirect('variationDetails', pk=pk)
        except requests.exceptions.RequestException as e:
            print(e)
            return redirect('variation')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login') 
    return redirect('variation')

def variationDetails(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYVariation")
    Variation = []
    responses =''
    Status=''

    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                Variation.append(json.loads(output_json))
                for product in Variation:
                    if product['Variation_No_'] == pk:
                        responses = product
                        Status = product['Status']
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    
    ctx = {"res":responses,"status":Status}
    return render(request,'variationDetails.html',ctx)

def variationGateway(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYVariation")
    Products = []
    paid=''
    responses=''
    Status = ''
    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                Products.append(json.loads(output_json))
                for product in Products:
                    if product['Variation_No_'] == pk:
                        responses = product
                        Status = product['Status']
                        paid = product['Paid']
        if request.method == 'POST':
            if paid == True:
                messages.success(request,"Payment Received successfully")
                return redirect('variationDetails', pk=pk)
            if paid == False:
                messages.info(request,"Payment not received, Try again.")
                return redirect('variationGateway', pk=pk)
            
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    ctx = {"res":responses,"status":Status}
    return render(request,'variationGateway.html',ctx)


