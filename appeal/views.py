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
    Access_Point= config.O_DATA.format("/QYRegistration")
    OpenProducts = []
    Pending = []
    Approved = []
    Rejected =[]
    ApprovedAppeal =[]
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
        AppealResponse = session.get(Access_Point, timeout=10).json()
        for res in AppealResponse['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                ApprovedAppeal.append(json.loads(output_json))
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
    "rejectedCount":rejectedCount,"rejected":Rejected,"product":ApprovedAppeal}
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

def ApplyAppeal(request):
    if request.method == 'POST':
        try:
            appNo = ''
            myAction = 'insert'
            prodNo = request.POST.get('prodNo')
            response = config.CLIENT.service.FnAppeal(appNo,myAction,request.session['UserID'],prodNo)
            print(response)
            if response == True:
                messages.success(request,"Request Successful")
                return redirect('appeal')
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

def SubmitAppeal(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.SubmitAppeal(pk,request.session['UserID'])
            print(response)
            if response == True:
                messages.success(request,"Document submitted successfully.")
                return redirect('appealDetails', pk=pk)
            else:
                print("Not sent")
                return redirect ('appealDetails',pk=pk)
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('Registration')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        except Exception as e:
            messages.error(request,e)
            return redirect ('appealDetails',pk=pk)
    return redirect('appealDetails', pk=pk)
