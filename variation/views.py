from django.shortcuts import render,redirect
import requests
import json
from django.conf import settings as config
from django.contrib import messages
from django.views import View

# Create your views here.
class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response

class variation(UserObjectMixin,View):
    def get(self,request):
        try:
            session = requests.Session()
            session.auth = config.AUTHS
            userId =request.session['UserID']
            variation= config.O_DATA.format(f"/QYVariation?$filter=User_code%20eq%20%27{userId}%27")
            response = self.get_object(variation)
            OpenProducts = [x for x in response['value'] if x['Status'] == 'Open']
            Pending = [x for x in response['value'] if x['Status'] == 'Processing']
            Approved = [x for x in response['value'] if x['Status'] == 'Approved']
            Rejected = [x for x in response['value'] if x['Status'] == 'Rejected']

            Access_Point= config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27")
            VarResponse = self.get_object(Access_Point)
            ApprovedVariation = [x for x in VarResponse['value'] if x['Status'] == 'Approved']
            
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
        "rejectedCount":rejectedCount,"rejected":Rejected,"product":ApprovedVariation}
        return render(request,"variation.html",ctx)
    def post(self, request):
        if request.method == 'POST':
            try:
                varNo = request.POST.get('varNo')
                prodNo = request.POST.get('prodNo')
                myAction = request.POST.get('myAction')
                dosageForms = request.POST.get('dosageForms')
                typeofChange = request.POST.get('typeofChange')
                otherApplications = request.POST.get('otherApplications')
                scope = request.POST.get('scope')
                background = request.POST.get('background')
                present = request.POST.get('background')
                proposed = request.POST.get('proposed')


                response = config.CLIENT.service.FnVariation(varNo,myAction,request.session['UserID'],dosageForms,prodNo,
                typeofChange,otherApplications,scope,background,present,proposed)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully")
                    return redirect('variation')
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('variation')
            except KeyError as e:
                messages.info(request,"Session Expired, Login Again")
                print(e)
                return redirect('login') 
        return redirect('variation')


    
class  variationDetails(UserObjectMixin,View):
    def get(self, request,pk):
        try:
            userID = request.session['UserID']
            Access_Point = config.O_DATA.format(f"/QYVariation?$filter=User_code%20eq%20%27{userID}%27%20and%20Variation_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            
            for res in response['value']:
                responses = res
                Status = res['Status']
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('variation')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        
        ctx = {"res":responses,"status":Status}
        return render(request,'variationDetails.html',ctx)

class variationGateway(UserObjectMixin,View):
    def get(self,request,pk):
        try:
            userID = request.session['UserID']
            Access_Point = config.O_DATA.format(f"/QYVariation?$filter=User_code%20eq%20%27{userID}%27%20and%20Variation_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']              
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('variation')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        ctx = {"res":responses,"status":Status}
        return render(request,'variationGateway.html',ctx)
    def post(self,request,pk):
        if request.method == 'POST':
            try:
                transactionCode = request.POST.get('transactionCode')
                currency = request.POST.get('currency')

                if not transactionCode:
                    messages.error(request, "Transaction Code can't be empty.")
                    return redirect('variationGateway', pk=pk)
                if not currency:
                    messages.error(request, "Currency code missing please contact the system admin")
                    return redirect('variationGateway', pk=pk)
                response = config.CLIENT.service.FnConfirmPayment(transactionCode,currency,pk,request.session['UserID'])
                print(response)
                if response == True:
                    messages.success(request,"Payment was successful. You can now submit your application.")
                    return redirect('variationDetails', pk=pk)
                else:
                    messages.error("Payment Not sent. Try Again.")
                    return redirect('variationGateway', pk=pk)
            except requests.exceptions.RequestException as e:
                messages.error(request,e)
                print(e)
                return redirect('variationGateway', pk=pk)
            except KeyError as e:
                messages.info(request,"Session Expired, Login Again")
                print(e)
                return redirect('login')
            except Exception as e:
                messages.error(request,e)
                return redirect('variationGateway', pk=pk)
        return redirect('variationGateway', pk=pk)

def SubmitVariation(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.SubmitVariation(pk,request.session['UserID'])
            print(response)
            if response == True:
                messages.success(request,"Document submitted successfully.")
                return redirect('variationDetails', pk=pk)
            else:
                print("Not sent")
                return redirect ('variationDetails',pk=pk)
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
            return redirect ('variationDetails',pk=pk)
    return redirect('variationDetails', pk=pk)
