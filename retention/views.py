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
            VMDRegistrationNumber = request.POST.get('VMDRegistrationNumber')
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

            response = config.CLIENT.service.Retension(retNo,myAction,request.session['UserID'],pk,VMDRegistrationNumber,
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