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
def productDetails(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYRegistration")
    ManufacturesParticulars = config.O_DATA.format("/QYManufactureParticulers")
    Countries = config.O_DATA.format("/QYCountries")
    ActiveIngredients = config.O_DATA.format("/QYActiveingredients")
    CountriesRegistered = config.O_DATA.format("/QYCountriesRegistered")
    InactiveIngredients = config.O_DATA.format("/QYInactiveIngredients")
    Products = []
    Manufacturer = []
    ActiveIngredient = []
    CountriesRegister = []
    InactiveIngredient = []
    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                Products.append(json.loads(output_json))
                for product in Products:
                    if product['ProductNo'] == pk and product['I_Agree'] == True:
                        responses = product
                        Status = product['Status']
                        productClass = product['Veterinary_Classes']
                    if product['ProductNo'] == pk and product['I_Agree'] == False:
                        messages.error(request,"You have not agreed to the terms and conditions. You can not continue with registration. Your data will be deleted")
                        return redirect('Registration')
        ManufacturerResponse = session.get(ManufacturesParticulars, timeout=10).json()
        for manufacturer in ManufacturerResponse['value']:
            if manufacturer['User_code'] == request.session['UserID'] and manufacturer['No'] == pk:
                output_json = json.dumps(manufacturer)
                Manufacturer.append(json.loads(output_json))
        CountryResponse = session.get(Countries, timeout=10).json()
        resCountry = CountryResponse['value']
        ActiveIngredientResponse = session.get(ActiveIngredients, timeout=10).json()
        for ingredient in ActiveIngredientResponse['value']:
            if ingredient['User_code'] == request.session['UserID'] and ingredient['No'] == pk:
                output_json = json.dumps(ingredient)
                ActiveIngredient.append(json.loads(output_json))
        CountriesRegisteredResponse = session.get(CountriesRegistered, timeout=10).json()
        for country in CountriesRegisteredResponse['value']:
            if country['User_code'] == request.session['UserID'] and country['No'] == pk:
                output_json = json.dumps(country)
                CountriesRegister.append(json.loads(output_json))
        InactiveIngredientsResponse = session.get(InactiveIngredients, timeout=10).json()
        for Inactive in InactiveIngredientsResponse['value']:
            if Inactive['User_code'] == request.session['UserID'] and Inactive['No'] == pk:
                output_json = json.dumps(Inactive)
                InactiveIngredient.append(json.loads(output_json))
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    
    ctx = {"res":responses,"status":Status,"class":productClass,
    "manufacturer":Manufacturer,"country":resCountry,
    "ActiveIngredient":ActiveIngredient,"CountriesRegister":CountriesRegister,
    "InactiveIngredient":InactiveIngredient}
    return render(request,'productDetails.html',ctx)

def ManufacturesParticulars(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            manufacturerName = request.POST.get('manufacturerName')
            plantAddress = request.POST.get('plantAddress')
            activity = request.POST.get('activity')
            userId = request.session['UserID']
            try:
                response = config.CLIENT.service.ManufacuresParticulars(prodNo,myAction,manufacturerName,plantAddress,
                activity,userId)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully. Click Add New to create more  records")
                    return redirect('productDetails',pk=pk)
                else:
                    print("Not sent")
                    return redirect ('productDetails',pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('productDetails', pk=prodNo)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect('productDetails',pk=pk)

def activeIngredients(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            ingredientName = request.POST.get('ingredientName')
            quantityPerDose = request.POST.get('quantityPerDose')
            specification = request.POST.get('specification')
            userId = request.session['UserID']
            try:
                response = config.CLIENT.service.ActiveIngredients(prodNo,myAction,ingredientName,quantityPerDose,
                specification,userId)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully. Click Add New to create more records")
                    return redirect('productDetails',pk=pk)
                else:
                    print("Not sent")
                    return redirect ('productDetails',pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('productDetails', pk=prodNo)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect ('productDetails',pk=pk)

def InactiveIngredients(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            userId = request.session['UserID']
            ingredientName = request.POST.get('ingredientName')
            quantityPerDose = request.POST.get('quantityPerDose')
            specification = request.POST.get('specification')
            reasonForInclusion =request.POST.get('reasonForInclusion')
            
            try:
                response = config.CLIENT.service.InactiveIngredient(prodNo,myAction,userId,ingredientName,quantityPerDose,
                specification,reasonForInclusion)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully. Click Add New to create more  records")
                    return redirect('productDetails',pk=pk)
                else:
                    print("Not sent")
                    return redirect ('productDetails',pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('productDetails', pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect ('productDetails',pk=pk)
def CountryRegistered(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            country = request.POST.get('country')
            userId = request.session['UserID']
            
            try:
                response = config.CLIENT.service.CountriesRegistered(prodNo,myAction,country,userId)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully. Click Add New to create more records")
                    return redirect('productDetails',pk=pk)
                else:
                    print("Not sent")
                    return redirect ('productDetails',pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('productDetails', pk=prodNo)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect ('productDetails',pk=pk)