from django.shortcuts import render,redirect
import requests
import json
from django.contrib import messages
from django.conf import settings as config

# Create your views here.
def RenewalRequest(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Retention= config.O_DATA.format("/QYRenewal")
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
    return render (request,'renew.html',ctx)

def renewDetails(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYRenewal")
    Retension = []
    responses =''
    Status=''

    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                Retension.append(json.loads(output_json))
                for product in Retension:
                    if product['Renewal_No_'] == pk:
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
    return render(request,"renewDetails.html",ctx)

def ApplyRenewal(request,pk,id):
    if request.method == 'POST':
        try:
            renNo = pk
            myAction = 'modify'

            response = config.CLIENT.service.Renewal(renNo,myAction,request.session['UserID'],id)
            print(response)
            if response == True:
                messages.success(request,"Saved Successfully")
                return redirect('renewDetails', pk=pk)
        except requests.exceptions.RequestException as e:
            print(e)
            return redirect('renew')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login') 
    return redirect('renew')

def renewPayment(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.FnRegistrationPayment(pk,request.session['UserID'])
            print("pk:",pk)
            print(request.session['UserID'])
            print("response = ",response)

            if response == True:
                messages.success(request,"Please Make Your payment and click confirm payment.")
                return redirect('renewGateway', pk=pk)
            else:
                print("Not sent")
                messages.error(request,"Failed.")
                return redirect ('renewDetails',pk=pk)
        except Exception as e:
            print(e)
            messages.info(request,e)
            return redirect('renewDetails', pk=pk)
    return redirect('renewDetails', pk=pk)


def renewGateway(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYRenewal")
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
                    if product['Renewal_No_'] == pk:
                        responses = product
                        Status = product['Status']
                        paid = product['Paid']
        if request.method == 'POST':
            if paid == True:
                messages.success(request,"Payment Received successfully")
                return redirect('renewDetails', pk=pk)
            if paid == False:
                messages.info(request,"Payment not received, Try again.")
                return redirect('renewGateway', pk=pk)
            
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    ctx = {"res":responses,"status":Status}
    return render(request,'renewGateway.html',ctx)

def SubmitRenewal(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.SubmitRenewal(pk,request.session['UserID'])
            print(response)
            if response == True:
                messages.success(request,"Document submitted successfully.")
                return redirect('renewDetails', pk=pk)
            else:
                print("Not sent")
                return redirect ('renewDetails',pk=pk)
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
            return redirect ('renewDetails',pk=pk)
    return redirect('renewDetails', pk=pk)
