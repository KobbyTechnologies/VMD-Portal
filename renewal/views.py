from django.shortcuts import render,redirect
import requests
import json
from django.contrib import messages
from django.conf import settings as config
import base64

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
    Attachments = config.O_DATA.format("/QYRequiredDocuments")
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
        AttachResponse = session.get(Attachments, timeout=10).json()
        attach = AttachResponse['value']
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    
    ctx = {"res":responses,"status":Status,"attach":attach}
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

def RenewAttachement(request, pk):
    if request.method == "POST":
        try:
            attach = request.FILES.get('attachment')
            filename = request.POST.get('filename')
            tableID = 52177996
            attachment = base64.b64encode(attach.read())
            try:
                response = config.CLIENT.service.Attachement(
                    pk, filename, attachment, tableID)
                print(response)
                if response == True:
                    messages.success(request, "Upload Successful")
                    return redirect('renewDetails', pk=pk)
                else:
                    messages.error(request, "Failed, Try Again")
                    return redirect('renewDetails', pk=pk)
            except Exception as e:
                messages.error(request, e)
                print(e)
                return redirect('renewDetails', pk=pk)
        except Exception as e:
            print(e)
            return redirect('renewDetails', pk=pk)
    return redirect('renewDetails', pk=pk)