from django.shortcuts import render,redirect
import requests
import json
from django.contrib import messages
from django.conf import settings as config
import base64
from django.views import View

# Create your views here.
class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response

class RenewalRequest(UserObjectMixin,View):
    def get(self,request):
        try:
            session = requests.Session()
            session.auth = config.AUTHS
            userId = request.session['UserID']
            Renewal= config.O_DATA.format(f"/QYRenewal?$filter=User_code%20eq%20%27{userId}%27")
            response = self.get_object(Renewal)
            OpenProducts = [x for x in response['value'] if x['Status'] == 'Open']
            Pending = [x for x in response['value'] if x['Status'] == 'Processing']
            Approved = [x for x in response['value'] if x['Status'] == 'Approved']
            Rejected = [x for x in response['value'] if x['Status'] == 'Rejected']

            Access_Point= config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27")
            RenewalResponse = self.get_object(Access_Point)
            ApproveRenewal = [x for x in RenewalResponse['value'] if x['Status'] == 'Approved']

        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('applications')
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
        "rejectedCount":rejectedCount,"rejected":Rejected,"product":ApproveRenewal}
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

class  ApplyRenewal(UserObjectMixin,View):
    def post(self, request):
        if request.method == 'POST':
            try:
                renNo = request.POST.get('renNo')
                myAction = request.POST.get('myAction')
                prodNo = request.POST.get('prodNo')
                response = config.CLIENT.service.Renewal(renNo,myAction,request.session['UserID'],prodNo)
                print(response)
                if response == True:
                    messages.success(request,"Request Successful")
                    return redirect('renew')
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