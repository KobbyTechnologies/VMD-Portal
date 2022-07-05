from django.shortcuts import render
import requests
from django.conf import settings as config
import json
from django.contrib import messages
from django.shortcuts import redirect, render

# Create your views here.
def registrationRetention(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Retention= config.O_DATA.format("/QYRetension")
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
    return render(request,"retention.html",ctx)

def ApplyRetention(request,pk):
    if request.method == 'POST':
        try:
            retNo = ''
            myAction = 'insert'
            changesToTheProduct = request.POST.get('changesToTheProduct')
            variation = request.POST.get('variation')
            iAgree = eval(request.POST.get('iAgree'))
            VariationNumber = request.POST.get('VariationNumber')

            if not iAgree:
                iAgree = False
            if not variation:
                variation = False
            if not VariationNumber:
                VariationNumber = ''

            response = config.CLIENT.service.Retension(retNo,myAction,request.session['UserID'],pk,
            VariationNumber,changesToTheProduct,variation,iAgree)
            print(response)
            messages.success(request,"Saved Successfully")
            return redirect('productDetails', pk=pk)
        except requests.exceptions.RequestException as e:
            print(e)
            return redirect('retention')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login') 
    return redirect('retention')

def retentionDetails(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYRetension")
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
                    if product['ProductNo'] == pk:
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
    return render(request,'RetentionDetails.html',ctx)

def retentionPayment(request,pk,id):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.FnRegistrationPayment(pk,request.session['UserID'])
            print("pk:",pk)
            print(request.session['UserID'])
            print("response = ",response)

            if response == True:
                messages.success(request,"Please Make Your payment and click confirm payment.")
                return redirect('retentionGateway', pk=pk)
            else:
                print("Not sent")
                messages.error(request,"Failed.")
                return redirect ('retentionDetails',pk=id)
        except Exception as e:
            print(e)
            messages.info(request,e)
            return redirect('retentionDetails', pk=id)
    return redirect('retentionDetails', pk=id)


def retentionGateway(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYRetension")
    Products = []
    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                Products.append(json.loads(output_json))
                for product in Products:
                    if product['ProductNo'] == pk:
                        responses = product
                        Status = product['Status']
                        paid = product['Paid']
        if request.method == 'POST':
            if paid == True:
                messages.success(request,"Payment Received successfully")
                return redirect('retentionDetails', pk=pk)
            if paid == False:
                messages.info(request,"Payment not received, Try again.")
                return redirect('retentionGateway', pk=pk)
            
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    ctx = {"res":responses,"status":Status}
    return render(request,'retentionGateway.html',ctx)