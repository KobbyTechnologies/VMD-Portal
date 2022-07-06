import re
from django.shortcuts import render, redirect
import requests
import json
from django.conf import settings as config
from django.contrib import messages

# Create your views here.
def GMPApplication(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Retention= config.O_DATA.format("/QYGMP")
    CountriesRegistered = config.O_DATA.format("/QYCountries")
    OpenProducts = []
    Pending = []
    Approved = []
    Rejected =[]
    try:
        response = session.get(Retention, timeout=10).json()
        CountryResponse = session.get(CountriesRegistered, timeout=10).json()
        resCountry = CountryResponse['value']
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
    "rejectedCount":rejectedCount,"rejected":Rejected,
    "country":resCountry}
    return render(request,'gmp.html',ctx)

def ApplyGMP(request):
    if request.method == "POST":
        try:
            gmpNo = ''
            myAction= 'insert'
            SitePhysicalAddress = request.POST.get('SitePhysicalAddress')
            SiteCountry = request.POST.get('SiteCountry')
            SiteTelephone = request.POST.get('SiteTelephone')
            SiteMobile = request.POST.get('SiteMobile')
            SiteEmail = request.POST.get('SiteEmail')
            isContact = request.POST.get('isContact')
            ContactName =request.POST.get('ContactName')
            ContactTel = request.POST.get('ContactTel')
            ContactEmail = request.POST.get('ContactEmail')
            VeterinaryMedicines = int(request.POST.get('VeterinaryMedicines'))
            TypeOfInspection = int(request.POST.get('TypeOfInspection'))
            stateOther = request.POST.get('StateOther')
            iAgree = eval(request.POST.get('iAgree'))

            if not iAgree:
                iAgree = False
            if not ContactName:
                ContactName = ''

            if not ContactTel:
                ContactTel = ''

            if not ContactEmail:
                ContactEmail = ''

            if not stateOther:
                stateOther = ''

            response = config.CLIENT.service.GMP(gmpNo,myAction,request.session['UserID'],SitePhysicalAddress,
            SiteCountry,SiteTelephone,SiteMobile,SiteEmail,isContact,ContactName,ContactTel,ContactEmail,
            VeterinaryMedicines,TypeOfInspection,stateOther,iAgree
            )
            print(response)
            if response == True:
                messages.success(request,"Saved Successfully")
                return redirect('gmp')

        except requests.exceptions.RequestException as e:
            print(e)
            return redirect('dashboard')
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect('gmp')

def GMPDetails(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYGMP")
    Lines = config.O_DATA.format("/QYLinestobeInspected")
    gmp = []
    Line = []
    responses =''
    Status=''

    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                gmp.append(json.loads(output_json))
                for product in gmp:
                    if product['GMP_No_'] == pk and product['I_Agree'] == True:
                        responses = product
                        Status = product['Status']
                    if product['GMP_No_'] == pk and product['I_Agree'] == False:
                        messages.error(request,"You have not agreed to the terms and conditions. You can not continue with registration. Your data will be deleted")
                        return redirect('gmp')
        linesResponse = session.get(Lines, timeout=10).json()
        for line in linesResponse['value']:
            if line['User_code'] == request.session['UserID'] and line['No'] == pk:
                output_json = json.dumps(line)
                Line.append(json.loads(output_json))
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    
    ctx = {"res":responses,"status":Status,"line":Line}
    return render(request,"gmpDetails.html",ctx)

def linesToInspect(request,pk):
    if request.method == "POST":
        try:
            myAction= 'insert'
            DosageForm = int(request.POST.get('DosageForm'))
            otherDosage = request.POST.get('otherDosage')
            Activity = int(request.POST.get('Activity'))

            if not otherDosage:
                otherDosage = ''
            try:
                response = config.CLIENT.service.LinesInspected(pk,myAction,request.session['UserID'],DosageForm,
                otherDosage,Activity)
                print(response)
                if response == True:
                    messages.success(request,"Saved Successfully")
                    return redirect('GMPDetails',pk=pk)
            except Exception as e:
                print(e)
                messages.error(request,e)
                return redirect('GMPDetails',pk=pk)
        except KeyError as e:
            messages.info(request,"Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect('GMPDetails',pk=pk)

def GMPGateway(request,pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYGMP")
    Products = []
    paid=''
    responses=''
    Status = ''
    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID']:
                output_json = json.dumps(res)
                Products.append(json.loads(output_json))
                for product in Products:
                    if product['GMP_No_'] == pk:
                        responses = product
                        Status = product['Status']
                        paid = product['Paid']
        if request.method == 'POST':
            if paid == True:
                messages.success(request,"Payment Received successfully")
                return redirect('GMPDetails', pk=pk)
            if paid == False:
                messages.info(request,"Payment not received, Try again.")
                return redirect('GMPGateway', pk=pk)
            
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('Registration')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    ctx = {"res":responses,"status":Status}
    return render(request,'GMPGateway.html',ctx)


def GMPPayment(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.FnRegistrationPayment(pk,request.session['UserID'])
            print("pk:",pk)
            print(request.session['UserID'])
            print("response = ",response)

            if response == True:
                messages.success(request,"Please Make Your payment and click confirm payment.")
                return redirect('GMPGateway', pk=pk)
            else:
                print("Not sent")
                messages.error(request,"Failed.")
                return redirect ('GMPDetails',pk=pk)
        except Exception as e:
            print(e)
            messages.info(request,e)
            return redirect('GMPDetails', pk=pk)
    return redirect('GMPDetails', pk=pk)

def SubmitGMP(request,pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.SubmitGMP(pk,request.session['UserID'])
            print(response)
            if response == True:
                messages.success(request,"Document submitted successfully.")
                return redirect('GMPDetails', pk=pk)
            else:
                print("Not sent")
                return redirect ('GMPDetails',pk=pk)
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
            return redirect ('GMPDetails',pk=pk)
    return redirect('GMPDetails', pk=pk)

    # To check against the user code to see whether there are products registered