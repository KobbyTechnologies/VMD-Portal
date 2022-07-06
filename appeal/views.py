from django.shortcuts import render,redirect
import json
import requests
from django.conf import settings as config
from django.contrib import messages
from datetime import date, datetime

# Create your views here.
def appealRequest(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Retention= config.O_DATA.format("/QYAppeal")
    OpenProducts = []
    Pending = []
    Approved = []
    Rejected =[]
    try:
        response = session.get(Retention, timeout=10).json()

        for res in response['value']:
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Open':
                output_json = json.dumps(res)
                OpenProducts.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Processing':
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
    return render(request,'appeal.html',ctx)


def appealDetails(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYAppeal")
    Appeal = []
    responses =''
    Status=''

    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                Appeal.append(json.loads(output_json))
                for product in Appeal:
                    if product['Appeal_No_'] == pk:
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

    return render(request,"appealDetails.html",ctx)

def ApplyAppeal(request,pk,id):
    if request.method == 'POST':
        try:
            myAction = 'modify'

            response = config.CLIENT.service.FnAppeal(pk,myAction,request.session['UserID'],id)
            print(response)
            return redirect('appealDetails',pk=pk)
        except requests.exceptions.RequestException as e:
            print(e)
            messages.error(request,e)
            return redirect('appeal')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login') 
    return redirect('appeal')

def appealGateway(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYAppeal")
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
                    if product['Appeal_No_'] == pk:
                        responses = product
                        Status = product['Status']
                        paid = product['Paid']
        if request.method == 'POST':
            if paid == True:
                messages.success(request,"Payment Received successfully")
                return redirect('appealDetails', pk=pk)
            if paid == False:
                messages.info(request,"Payment not received, Try again.")
                return redirect('appealGateway', pk=pk)

    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    ctx = {"res":responses,"status":Status}
    return render(request,'appealGateway.html',ctx)

def appealPayment(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.FnRegistrationPayment(pk,request.session['UserID'])
            print("pk:",pk)
            print(request.session['UserID'])
            print("response = ",response)

            if response == True:
                messages.success(request,"Please Make Your payment and click confirm payment.")
                return redirect('appealGateway', pk=pk)
            else:
                print("Not sent")
                messages.error(request,"Failed.")
                return redirect ('appealDetails',pk=pk)
        except Exception as e:
            print(e)
            messages.info(request,e)
            return redirect('appealDetails', pk=pk)
    return redirect('appealDetails', pk=pk)