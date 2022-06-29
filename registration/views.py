from django.shortcuts import redirect, render
from django.conf import settings as config
import requests 
from django.contrib import messages
import json
from datetime import date, datetime
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
    Ingredients = config.O_DATA.format("/QYIngredients")
    CountriesRegistered = config.O_DATA.format("/QYCountriesRegistered")
    MarketingAuthorisation = config.O_DATA.format("/QYMarketingAuthorisation")
    FeedAdditives = config.O_DATA.format("/QYAddictives")
    Methods = config.O_DATA.format("/QYMethods")
    Products = []
    Additive = []
    Method = []
    Manufacturer = []
    Ingredient = []
    CountriesRegister = []
    Marketing = []
    responses =''
    Status=''
    productClass=''
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
        IngredientResponse = session.get(Ingredients, timeout=10).json()
        for ingredient in IngredientResponse['value']:
            if ingredient['User_code'] == request.session['UserID'] and ingredient['No'] == pk:
                output_json = json.dumps(ingredient)
                Ingredient.append(json.loads(output_json))
        CountriesRegisteredResponse = session.get(CountriesRegistered, timeout=10).json()
        for country in CountriesRegisteredResponse['value']:
            if country['User_code'] == request.session['UserID'] and country['No'] == pk:
                output_json = json.dumps(country)
                CountriesRegister.append(json.loads(output_json))

        MarketingAuthorisationResponse = session.get(MarketingAuthorisation, timeout=10).json()
        for marketing in MarketingAuthorisationResponse['value']:
            if marketing['User_code'] == request.session['UserID'] and marketing['Country_No_'] == pk:
                output_json = json.dumps(marketing)
                Marketing.append(json.loads(output_json))
        AdditiveResponse = session.get(FeedAdditives, timeout=10).json()
        for additive in AdditiveResponse['value']:
            if additive['User_code'] == request.session['UserID'] and additive['No'] == pk:
                output_json = json.dumps(additive)
                Additive.append(json.loads(output_json))
        MethodResponse = session.get(Methods, timeout=10).json()
        for method in MethodResponse['value']:
            if method['User_Code'] == request.session['UserID'] and method['No'] == pk:
                output_json = json.dumps(method)
                Method.append(json.loads(output_json))
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
    "CountriesRegister":CountriesRegister,
    "marketing":Marketing,'ingredient':Ingredient,"additive":Additive,"method":Method}
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

def Ingredients(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            ingredientType = request.POST.get('ingredientType')
            ingredientName = request.POST.get('ingredientName')
            quantityPerDose = request.POST.get('quantityPerDose')
            strengthOfIngredient = request.POST.get('strengthOfIngredient')
            MolecularFormula = request.POST.get('MolecularFormula')
            MolecularWeight = request.POST.get('MolecularWeight')
            Proportion = request.POST.get('Proportion')
            ReasonForInclusion= request.POST.get('ReasonForInclusion')
            specification = request.POST.get('specification')
            userId = request.session['UserID']
            if not ReasonForInclusion:
                ReasonForInclusion = ''
            try:
                response = config.CLIENT.service.Ingredients(prodNo,myAction,ingredientName,ingredientType,ReasonForInclusion,quantityPerDose,
                Proportion,MolecularFormula,MolecularWeight,specification,strengthOfIngredient,userId)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully.")
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

def MarketingAuthorization(request,pk):
    if request.method == 'POST':
        try:
            myAction = request.POST.get('myAction')
            userId = request.session['UserID']
            AuthorisationStatus = request.POST.get('AuthorisationStatus')
            MarketingCountry = request.POST.get('MarketingCountry')
            DateAuthorisation = datetime.strptime(request.POST.get('DateAuthorisation'), '%Y-%m-%d').date()
            AuthorisationNumber = request.POST.get('AuthorisationNumber')
            AuthorisationReason = request.POST.get('AuthorisationReason')
            ProprietaryName = request.POST.get('ProprietaryName')

            if not AuthorisationReason:
                AuthorisationReason = ''
            if not AuthorisationNumber:
                AuthorisationNumber = ''
            if not ProprietaryName:
                ProprietaryName = ''
            try:
                response = config.CLIENT.service.MarketingAuthorisation(pk,myAction,userId,AuthorisationStatus,
                MarketingCountry,DateAuthorisation,AuthorisationNumber,AuthorisationReason,ProprietaryName)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully")
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

def makePayment(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.FnRegistrationPayment(pk,request.session['UserID'])
            print(pk)
            print(request.session['UserID'])
            print("response = ",response)
            messages.success(request,"Saved Successfully")
            # if response == True:
            #     return redirect('PaymentGateway', pk=pk)
            # else:
            #     print("Not sent")
            #     return redirect ('productDetails',pk=pk)
        except requests.exceptions.RequestException as e:
            print(e)
            return redirect('productDetails', pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login') 
    return redirect('productDetails', pk=pk)

def MyApplications(request):
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
    return render(request,'applications.html')