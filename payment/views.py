from django.shortcuts import redirect, render
from django.conf import settings as config
import requests 
from django.contrib import messages
import json
from datetime import date, datetime

# Create your views here.
def PaymentGateway(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYRegistration")
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
                        productClass = product['Veterinary_Classes']
                        paid = product['Paid']
        if request.method == 'POST':
            if paid == True:
                messages.success(request,"Payment Received successfully")
                return redirect('productDetails', pk=pk)
            if paid == False:
                messages.info(request,"Payment not received, Try again.")
                return redirect('PaymentGateway', pk=pk)
            
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    ctx = {"res":responses,"status":Status,"class":productClass}
    return render(request,'gateway.html',ctx)