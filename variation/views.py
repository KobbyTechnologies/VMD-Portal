from django.shortcuts import render,redirect
import requests
import json
from django.conf import settings as config
from django.contrib import messages
from datetime import date, datetime

# Create your views here.
def variation(request):
    session = requests.Session()
    session.auth = config.AUTHS
    variation= config.O_DATA.format("/QYVariation")

    OpenProducts = []
    Pending = []
    Approved = []
    Rejected =[]
    try:
        response = session.get(variation, timeout=10).json()

        for res in response['value']:
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Open':
                output_json = json.dumps(res)
                OpenProducts.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Pending Approval':
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
    return render(request,"variation.html",ctx)

def ApplyVariation(request,pk):
    if request.method == 'POST':
        try:
            varNo = ''
            myAction = 'insert'
            dosageForms = request.POST.get('dosageForms')
            typeofChange = request.POST.get('typeofChange')
            otherApplications = request.POST.get('otherApplications')
            scope = request.POST.get('scope')
            background = request.POST.get('background')
            present = request.POST.get('background')
            proposed = request.POST.get('proposed')


            response = config.CLIENT.service.FnVariation(varNo,myAction,request.session['UserID'],dosageForms,pk,
            typeofChange,otherApplications,scope,background,present,proposed)
            print(response)
            messages.success(request,"Saved Successfully")
            return redirect('productDetails', pk=pk)
        except requests.exceptions.RequestException as e:
            print(e)
            return redirect('variation')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login') 

