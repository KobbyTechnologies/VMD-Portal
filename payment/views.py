from django.shortcuts import redirect, render
from django.conf import settings as config
import requests 
from django.contrib import messages
import json
from django.views import View

# Create your views here.

class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response

class PaymentGateway(UserObjectMixin,View):
    def get(self,request,pk):
        try:
            LTR_Name = request.session['LTR_Name']
            LTR_Email = request.session['LTR_Email']
            userID = request.session['UserID']
            Access_Point= Access_Point = config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userID}%27%20and%20ProductNo%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']
                productClass = res['Veterinary_Classes']                
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('productDetails', pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        ctx = {"res":responses,"status":Status,"class":productClass,"LTR_Name":LTR_Name,"LTR_Email":LTR_Email}
        return render(request,'gateway.html',ctx)
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                transactionCode = request.POST.get('transactionCode')
                currency = request.POST.get('currency')

                if not transactionCode:
                    messages.error(request, "Transaction Code can't be empty.")
                    return redirect('PaymentGateway', pk=pk)
                if not currency:
                    messages.error(request, "Currency code missing please contact the system admin")
                    return redirect('PaymentGateway', pk=pk)
                response = config.CLIENT.service.FnConfirmPayment(transactionCode,currency,pk,request.session['UserID'])
                print(response)
                if response == True:
                    messages.success(request,"Payment was successful. You can now submit your application.")
                    return redirect('productDetails', pk=pk)
                else:
                    messages.error("Payment Not sent. Try Again.")
                    return redirect('PaymentGateway', pk=pk)
            except requests.exceptions.RequestException as e:
                messages.error(request,e)
                print(e)
                return redirect('PaymentGateway', pk=pk)
            except KeyError as e:
                messages.info(request,"Session Expired, Login Again")
                print(e)
                return redirect('login')
            except Exception as e:
                messages.error(request,e)
                return redirect('PaymentGateway', pk=pk)
        return redirect('PaymentGateway', pk=pk)
