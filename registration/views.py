from tkinter.filedialog import Open
from django.shortcuts import redirect, render
from django.conf import settings as config
import requests 
from django.contrib import messages
import json

# Create your views here.

def registrationRequest(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Vet_Classes= config.O_DATA.format("/QYVertinaryclasses")
    Access_Point= config.O_DATA.format("/QYRegistration")
    OpenProducts = []
    Pending = []
    Approved = []
    Rejected =[]
    try:
        vet_response = session.get(Vet_Classes, timeout=10).json()
        response = session.get(Access_Point, timeout=10).json()
        product = vet_response['value']

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
    ctx = {"product": product,"openCount":openCount,"open":OpenProducts,
    "pendCount":pendCount,"pending":Pending,"appCount":appCount,"approved":Approved,
    "rejectedCount":rejectedCount,"rejected":Rejected}
    return render(request,'registration.html',ctx)

def myApplications(request,pk):
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
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    ctx = {"res":responses,"status":Status,"class":productClass}
    return render(request, "applications.html",ctx)

def registrationRenewal(request):
    return render(request,"renewal.html")

def productClass(request):
    if request.method == "POST":
        try:
            classCode = request.POST.get('vetClass')
            typeofManufacture = int(request.POST.get('typeofManufacture'))
            myAction = request.POST.get('myAction')
            userCode = request.session['UserID']
            prodNo = request.POST.get('prodNo')
        except ValueError:
            messages.error(request,"Missing Input")
            return redirect('Registration')
        except KeyError:
            messages.info(request,"Session Expired, Login Again")
            return redirect('login')
        if not prodNo:
            prodNo = ''
        try:
            response = config.CLIENT.service.FnClass(prodNo, classCode,typeofManufacture,myAction,userCode)
            print(response)
            if response == True:
                messages.success(request,"Successfully Added")
                return redirect('Registration')
        except Exception as e:
            messages.error(request, e)
            print(e)
            return redirect('Registration')
    return redirect('Registration')
