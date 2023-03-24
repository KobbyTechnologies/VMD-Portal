from django.shortcuts import render,redirect
import requests
import json
from django.contrib import messages
from django.conf import settings as config
import base64
from django.views import View
import io as BytesIO
from django.http import HttpResponse

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
            LTR_Name = request.session['LTR_Name']
            LTR_Email = request.session['LTR_Email']
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
        "rejectedCount":rejectedCount,"rejected":Rejected,"product":ApproveRenewal,"LTR_Name":LTR_Name,"LTR_Email":LTR_Email}
        return render (request,'renew.html',ctx)

class renewDetails(UserObjectMixin,View):
    def get(self,request,pk):
        try:
            userID = request.session['UserID']
            LTR_Name = request.session['LTR_Name']
            LTR_Email = request.session['LTR_Email']
            Access_Point = config.O_DATA.format(f"/QYRenewal?$filter=User_code%20eq%20%27{userID}%27%20and%20Renewal_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']

            Attachments = config.O_DATA.format("/QYRequiredDocuments")
            AttachResponse = self.get_object(Attachments)
            attach = AttachResponse['value']
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('Registration')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        
        ctx = {"res":responses,"status":Status,"attach":attach,"LTR_Name":LTR_Name,"LTR_Email":LTR_Email}
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


class renewGateway(UserObjectMixin,View):
    def get(self, request,pk):
        try:
            userID = request.session['UserID']
            LTR_Name = request.session['LTR_Name']
            LTR_Email = request.session['LTR_Email']
            Access_Point = config.O_DATA.format(f"/QYRenewal?$filter=User_code%20eq%20%27{userID}%27%20and%20Renewal_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('renewGateway',pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        ctx = {"res":responses,"status":Status,"LTR_Name":LTR_Name,"LTR_Email":LTR_Email}
        return render(request,'renewGateway.html',ctx)
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                transactionCode = request.POST.get('transactionCode')
                currency = request.POST.get('currency')

                if not transactionCode:
                    messages.error(request, "Transaction Code can't be empty.")
                    return redirect('renewGateway', pk=pk)
                if not currency:
                    messages.error(request, "Currency code missing please contact the system admin")
                    return redirect('renewGateway', pk=pk)
                response = config.CLIENT.service.FnConfirmPayment(transactionCode,currency,pk,request.session['UserID'])
                print(response)
                if response == True:
                    messages.success(request,"Payment was successful. You can now submit your application.")
                    return redirect('renewDetails', pk=pk)
                else:
                    messages.error(request, "Payment Not sent. Try Again.")
                    return redirect('renewGateway', pk=pk)
            except requests.exceptions.RequestException as e:
                messages.error(request,e)
                print(e)
                return redirect('renewGateway', pk=pk)
            except KeyError as e:
                messages.info(request,"Session Expired, Login Again")
                print(e)
                return redirect('login')
            except Exception as e:
                messages.error(request,e)
                return redirect('renewGateway', pk=pk)
        return redirect('renewGateway', pk=pk)

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
            # filename = request.FILES['attachment'].name
            name = request.POST.get('name')
            tableID = 52177996
            attachment = base64.b64encode(attach.read())

            try:
                response = config.CLIENT.service.Attachement(
                    pk, name, attachment, tableID)
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

def FNGenerateRenewalInvoice(request, pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.FNGenerateRenewalInvoice(pk)
            buffer = BytesIO.BytesIO()
            content = base64.b64decode(response)
            buffer.write(content)
            responses = HttpResponse(
                buffer.getvalue(),
                content_type="application/pdf",
            )
            responses['Content-Disposition'] = f'inline;filename={pk}'
            return responses
        except Exception as e:
            messages.error(request, e)
            print(e)
    return redirect('renewGateway', pk=pk)

    