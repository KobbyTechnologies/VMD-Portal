from django.shortcuts import redirect, render
from django.conf import settings as config
import requests 
from django.contrib import messages
import json
from datetime import  datetime
import base64
import io as BytesIO
from django.http import HttpResponse
from django.views import View
# Create your views here.

class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response

class registrationRequest(UserObjectMixin,View):
    def get(self,request):
        try:
            userId = request.session['UserID'] 
            Vet_Classes= config.O_DATA.format("/QYVertinaryclasses")
            vet_response = self.get_object(Vet_Classes)
            product = vet_response['value']

            Access_Point= config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27")
            response = self.get_object(Access_Point)
            OpenProducts = [x for x in response['value'] if x['Status'] == 'Open']
            Pending = [x for x in response['value'] if x['Status'] == 'Processing']
            Approved = [x for x in response['value'] if x['Status'] == 'Approved']
            Rejected = [x for x in response['value'] if x['Status'] == 'Rejected']

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

class myApplications(UserObjectMixin,View):
    def get(self, request,pk):
        try:
            userId = request.session['UserID']
            Access_Point = config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27%20and%20ProductNo%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']
                productClass = res['Veterinary_Classes']

            Country = config.O_DATA.format("/QYCountries")   
            CountryResponse = self.get_object(Country)
            resCountry = CountryResponse['value']
        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('applications')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        ctx = {"res":responses,"status":Status,"class":productClass,"country":resCountry}
        return render(request, "applications.html",ctx)


def productClass(request):
    if request.method == "POST":
        try:
            classCode = request.POST.get('vetClass')
            typeofManufacture = int(request.POST.get('typeofManufacture'))
            myAction = request.POST.get('myAction')
            userCode = request.session['UserID']
            prodNo = request.POST.get('prodNo')
            if not prodNo:
                prodNo = ''
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

class productDetails(UserObjectMixin,View):
    def get(self, request,pk):
        try:
            UserID=request.session['UserID']
            LTR_Name=request.session['LTR_Name']
            LTR_Email=request.session['LTR_Email']
            LTR_Country=request.session['Country']
            LTR_BS_No=request.session['Business_Registration_No_'] 
            userId = request.session['UserID']
            Access_Point = config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27%20and%20ProductNo%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']
                productClass = res['Veterinary_Classes']
                            
            ManufacturesParticulars = config.O_DATA.format(f"/QYManufactureParticulers?$filter=User_code%20eq%20%27{userId}%27%20and%20No%20eq%20%27{pk}%27")
            ManufacturerResponse = self.get_object(ManufacturesParticulars)
            Manufacturer = [x for x in ManufacturerResponse['value']]

            Countries = config.O_DATA.format("/QYCountries")
            CountryResponse = self.get_object(Countries)
            resCountry = CountryResponse['value']

            Ingredients = config.O_DATA.format(f"/QYIngredients?$filter=User_code%20eq%20%27{userId}%27%20and%20No%20eq%20%27{pk}%27")
            IngredientResponse = self.get_object(Ingredients)
            Ingredient = [x for x in IngredientResponse['value']]


            CountriesRegistered = config.O_DATA.format(f"/QYCountriesRegistered?$filter=User_code%20eq%20%27{userId}%27%20and%20No%20eq%20%27{pk}%27")
            CountriesRegisteredResponse = self.get_object(CountriesRegistered)  
            CountriesRegister = [x for x in CountriesRegisteredResponse['value']]

            MarketingAuthorisation = config.O_DATA.format(f"/QYMarketingAuthorisation?$filter=User_code%20eq%20%27{userId}%27%20and%20Country_No_%20eq%20%27{pk}%27")
            MarketingAuthorisationResponse = self.get_object(MarketingAuthorisation)
            Marketing = [x for x in MarketingAuthorisationResponse['value']]

            FeedAdditives = config.O_DATA.format(f"/QYAddictives?$filter=User_code%20eq%20%27{userId}%27%20and%20No%20eq%20%27{pk}%27")
            AdditiveResponse = self.get_object(FeedAdditives)
            Additive = [x for x in AdditiveResponse['value']]

            Methods = config.O_DATA.format(f"/QYMethods?$filter=User_Code%20eq%20%27{userId}%27%20and%20No%20eq%20%27{pk}%27")
            MethodResponse = self.get_object(Methods)
            Method = [x for x in MethodResponse['value']]

            Attachments = config.O_DATA.format("/QYRequiredDocuments")
            AttachResponse = self.get_object(Attachments)
            attach = AttachResponse['value']

            AllAttachments = config.O_DATA.format(f"/QYDocumentAttachments?$filter=No_%20eq%20%27{pk}%27%20and%20Table_ID%20eq%2052177996")
            AllAttachResponse = self.get_object(AllAttachments)
            Files = [x for x in AllAttachResponse['value']]

        except requests.exceptions.RequestException as e:
            messages.error(request,e)
            print(e)
            return redirect('login')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
        except Exception as e:
            messages.error(request,e)
            return redirect('login')
        
        ctx = {"res":responses,"status":Status,"class":productClass,
        "manufacturer":Manufacturer,"country":resCountry,'ingredient':Ingredient,
        "CountriesRegister":CountriesRegister,"marketing":Marketing,"additive":Additive,"method":Method,"files": Files,
        "UserID":UserID,"LTRName":LTR_Name,"LTR_Email":LTR_Email,"LTRBsNo":LTR_BS_No,"LTRCountry":LTR_Country,"attach":attach}
        
        return render(request,'productDetails.html',ctx)

def ManufacturesParticulars(request,pk):
    if request.method == 'POST':
        try:
            prodNo = pk
            myAction = request.POST.get('myAction')
            TypeOfManufacturer = int(request.POST.get('TypeOfManufacturer'))
            manufacturerOther = request.POST.get('manufacturerOther')
            manufacturerName = request.POST.get('manufacturerName')
            plantAddress = request.POST.get('plantAddress')
            country = request.POST.get('country')
            ManufacturerTelephone = request.POST.get('ManufacturerTelephone')
            ManufacturerEmail= request.POST.get('ManufacturerEmail')
            activity = int(request.POST.get('activity'))
            ManufacturerGMP = request.POST.get('ManufacturerGMP')
            userId = request.session['UserID']
            lineNo = request.POST.get('lineNo')

            if not manufacturerOther:
                manufacturerOther = ''
            
            if not ManufacturerGMP:
                ManufacturerGMP = ''

            try:
                response = config.CLIENT.service.ManufacuresParticulars(prodNo,myAction,TypeOfManufacturer,
                manufacturerOther,manufacturerName,plantAddress,country,ManufacturerTelephone,ManufacturerEmail,
                activity,ManufacturerGMP,userId,lineNo)
                print(response)
                if response == True:
                    messages.success(request,"Request Successful")
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
            Proportion = request.POST.get('Proportion')
            ReasonForInclusion= request.POST.get('ReasonForInclusion')
            specification = request.POST.get('specification')
            userId = request.session['UserID']
            lineNo = request.POST.get('lineNo')
            print(prodNo,myAction,ingredientType,ingredientName,quantityPerDose
            ,strengthOfIngredient,Proportion,ReasonForInclusion,specification,userId,lineNo)
            if not ReasonForInclusion:
                ReasonForInclusion = ''
            try:
                response = config.CLIENT.service.Ingredients(prodNo,myAction,ingredientName,ingredientType,ReasonForInclusion,quantityPerDose,
                Proportion,specification,strengthOfIngredient,userId,lineNo)
                print(response)
                if response == True:
                    messages.success(request,"Request Successful")
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
            lineNo = request.POST.get('lineNo')
            
            try:
                response = config.CLIENT.service.CountriesRegistered(prodNo,myAction,country,userId,lineNo)
                print(response)
                if response == True:
                    messages.success(request,"Request Successful")
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
            lineNo = request.POST.get('lineNo')

            if not AuthorisationReason:
                AuthorisationReason = ''
            if not AuthorisationNumber:
                AuthorisationNumber = ''
            if not ProprietaryName:
                ProprietaryName = ''
            try:
                response = config.CLIENT.service.MarketingAuthorisation(pk,myAction,userId,AuthorisationStatus,
                MarketingCountry,DateAuthorisation,AuthorisationNumber,AuthorisationReason,ProprietaryName,lineNo)
                print(response)
                if response == True:
                    messages.success(request,"Request Successful")
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

class makePayment(UserObjectMixin,View):
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                prodNo = pk
                userCode = request.session['UserID']

                response = config.CLIENT.service.FnRegistrationPayment(prodNo,userCode)
                print(prodNo,userCode,response)
                if response == True:
                    messages.success(request,"Please Make Your payment and click confirm payment.")
                    return redirect('PaymentGateway', pk=pk)
                if response == False:
                    messages.error(request,"False")
                    return redirect('productDetails', pk=pk)
            except KeyError as e:
                messages.info(request,"Session Expired, Login Again")
                print(e)
                return redirect('login')
            except Exception as e:
                print(e)
                messages.info(request,e)
                return redirect ('productDetails',pk=pk)
        return redirect('productDetails', pk=pk)

class MyApplications(UserObjectMixin):
    def get(self,request):
        try:
            userId = request.session['UserID']

            Vet_Classes= config.O_DATA.format("/QYVertinaryclasses")
            vet_response = self.get_object(Vet_Classes)
            product = vet_response['value']

            Access_Point= config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27")
            response = self.get_object(Access_Point)
            OpenProducts = [x for x in response['value'] if x['Status'] == 'Open']
            Pending = [x for x in response['value'] if x['Status'] == 'Processing']
            Approved = [x for x in response['value'] if x['Status'] == 'Approved']
            Rejected = [x for x in response['value'] if x['Status'] == 'Rejected']
            
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
        ctx = {"product": product,"openCount":openCount,"open":OpenProducts,
        "pendCount":pendCount,"pending":Pending,"appCount":appCount,"approved":Approved,
        "rejectedCount":rejectedCount,"rejected":Rejected}
        return render(request,'applications.html',ctx)

class allApplications(UserObjectMixin,View):
    def get(self, request):
        try:
            userId =request.session['UserID']
            Access_Point=  config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27")
            response = self.get_object(Access_Point)
            OpenProducts = [x for x in response['value'] if x['Status'] == 'Open']
            Pending = [x for x in response['value'] if x['Status'] == 'Processing']
            Approved = [x for x in response['value'] if x['Status'] == 'Approved']
            Rejected = [x for x in response['value'] if x['Status'] == 'Rejected']

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
        "rejectedCount":rejectedCount,"rejected":Rejected}
        return render(request,'submitted.html',ctx)


def SubmitRegistration(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.SubmitRegistration(pk,request.session['UserID'])
            print(response)
            if response == True:
                messages.success(request,"Document submitted successfully.")
                return redirect('productDetails', pk=pk)
            else:
                print("Not sent")
                return redirect ('productDetails',pk=pk)
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
            return redirect ('productDetails',pk=pk)
    return redirect('productDetails', pk=pk)

def Attachement(request, pk):
    if request.method == "POST":
        try:
            attach = request.FILES.get('attachment')
            filename = request.FILES['attachment'].name
            name = request.POST.get('name')
            tableID = 52177996
            attachment = base64.b64encode(attach.read())

            try:
                response = config.CLIENT.service.Attachement(
                    pk, filename,name, attachment, tableID)
                print(response)
                if response == True:
                    messages.success(request, "Upload Successful")
                    return redirect('productDetails', pk=pk)
                else:
                    messages.error(request, "Failed, Try Again")
                    return redirect('productDetails', pk=pk)
            except Exception as e:
                messages.error(request, e)
                print(e)
                return redirect('productDetails', pk=pk)
        except Exception as e:
            print(e)        
    return redirect('productDetails', pk=pk)

def FnDeleteDocumentAttachment(request,pk):
    if request.method == "POST":
        docID = int(request.POST.get('docID'))
        tableID= int(request.POST.get('tableID'))
        try:
            response = config.CLIENT.service.FnDeleteDocumentAttachment(
                pk,docID,tableID)
            print(response)
            if response == True:
                messages.success(request, "Deleted Successfully ")
                return redirect('productDetails', pk=pk)
        except Exception as e:
            messages.error(request, e)
            print(e)
    return redirect('productDetails', pk=pk)

def GenerateCertificate(request, pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.PrintCertificate(
                pk)
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
    return redirect('productDetails', pk=pk)