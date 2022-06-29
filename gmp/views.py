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
            VeterinaryMedicines = request.POST.get('VeterinaryMedicines')
            TypeOfInspection = request.POST.get('TypeOfInspection')
            stateOther = request.POST.get('StateOther')
            iAgree = eval(request.POST.get('iAgree'))

            if not iAgree:
                iAgree = False

            response = config.CLIENT.service.GMP(gmpNo,myAction,request.session['UserID'],SitePhysicalAddress,
            SiteCountry,SiteTelephone,SiteMobile,SiteEmail,isContact,ContactName,ContactTel,ContactEmail,
            VeterinaryMedicines,TypeOfInspection,stateOther,iAgree
            )
            print(response)
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
    return render(request,"gmpDetails.html")

    # To check against the user code to see whether there are products registered