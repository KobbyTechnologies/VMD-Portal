from django.shortcuts import render,redirect
import json
import requests
from django.conf import settings as config
from django.contrib import messages
from django.views import  View

# Create your views here.

class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response

class appealRequest(UserObjectMixin,View):
    def get(self,request):
        try:
            userID =request.session['UserID']
            Retention= config.O_DATA.format(f"/QYAppeal?$filter=User_code%20eq%20%27{userID}%27")
            response = self.get_object(Retention)
            openAppeal = [x for x in response['value'] if x['Status'] == 'Open']
            pendingAppeal = [x for x in response['value'] if x['Status'] == 'Processing']
            approvedAppeal = [x for x in response['value'] if x['Status'] == 'Approved']
            rejectedAppeal = [x for x in response['value'] if x['Status'] == 'Rejected']

            Access_Point= config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userID}%27")
            rejectedResponse = self.get_object(Access_Point)
            Rejected = [x for x in rejectedResponse['value'] if x['Status'] == 'Rejected']
            
        except Exception as e:
            messages.error(request,e)
            print(e)
            return redirect('login')
        openCount = len(openAppeal)
        pendCount = len(pendingAppeal)
        appCount = len(approvedAppeal)
        rejectedCount = len(rejectedAppeal)
        ctx = {"openCount":openCount,"open":openAppeal,
        "pendCount":pendCount,"pending":pendingAppeal,"appCount":appCount,"approved":approvedAppeal,
        "rejectedCount":rejectedCount,"rejected":rejectedAppeal,"product":Rejected}
        return render(request,'appeal.html',ctx)
    def post(self, request):
        if request.method == 'POST':
            try:
                appNo = request.POST.get('appNo')
                myAction = request.POST.get('myAction')
                prodNo = request.POST.get('prodNo')
                response = config.CLIENT.service.FnAppeal(appNo,myAction,request.session['UserID'],prodNo)
                print("response:",response)
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

class appealDetails(UserObjectMixin,View):
    def get(self, request,pk):
        try:
            userID =request.session['UserID']
            Access_Point= config.O_DATA.format(f"/QYAppeal?$filter=User_code%20eq%20%27{userID}%27%20and%20Appeal_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        except Exception as e:
            messages.error(request,e)
            print(e)
            return redirect('appeal')
            
        ctx = {"res":responses,"status":Status}
        return render(request,"appealDetails.html",ctx)
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                response = config.CLIENT.service.SubmitAppeal(pk,request.session['UserID'])
                print(response)
                if response == True:
                    messages.success(request,"Document submitted successfully.")
                    return redirect('appealDetails', pk=pk)
            except requests.exceptions.RequestException as e:
                messages.error(request,e)
                print(e)
                return redirect ('appealDetails',pk=pk)
            except KeyError as e:
                messages.info(request,"Session Expired, Login Again")
                print(e)
                return redirect('login')
            except Exception as e:
                messages.error(request,e)
                return redirect ('appealDetails',pk=pk)
        return redirect('appealDetails', pk=pk)

   

class appealGateway(UserObjectMixin,View):
    def get(self,request,pk):
        try:
            userID =request.session['UserID']
            Access_Point= config.O_DATA.format(f"/QYAppeal?$filter=User_code%20eq%20%27{userID}%27%20and%20Appeal_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('appealDetails', pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        ctx = {"res":responses,"status":Status}
        return render(request,'appealGateway.html',ctx)
    def post(self,request,pk):
        if request.method == 'POST':
            try:
                transactionCode = request.POST.get('transactionCode')
                currency = request.POST.get('currency')

                if not transactionCode:
                    messages.error(request, "Transaction Code can't be empty.")
                    return redirect('appealGateway',pk=pk)
                if not currency:
                    messages.error(request, "Currency code missing please contact the system admin")
                    return redirect('appealGateway',pk=pk)
                response = config.CLIENT.service.FnConfirmPayment(transactionCode,currency,pk,request.session['UserID'])
                print(response)
                if response == True:
                    messages.success(request,"Payment was successful. You can now submit your application.")
                    return redirect('appealDetails', pk=pk)
                else:
                    messages.error("Payment Not sent. Try Again.")
                    return redirect('appealGateway',pk=pk)
            except requests.exceptions.RequestException as e:
                messages.error(request,e)
                print(e)
                return redirect('appealGateway',pk=pk)
            except KeyError as e:
                messages.info(request,"Session Expired, Login Again")
                print(e)
                return redirect('login')
            except Exception as e:
                messages.error(request,e)
                return redirect('appealGateway',pk=pk)
        return redirect('appealGateway',pk=pk)

    
