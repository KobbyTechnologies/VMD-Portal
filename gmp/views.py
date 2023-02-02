import base64
from django.shortcuts import render, redirect
import requests
import json
from django.conf import settings as config
from django.contrib import messages
from django.views import View
import io as BytesIO
from django.http import HttpResponse
# Create your views here.


class UserObjectMixin(object):
    model = None
    session = requests.Session()
    session.auth = config.AUTHS

    def get_object(self, endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response


class GMPApplication(UserObjectMixin, View):
    def get(self, request):
        try:
            userID = request.session['UserID']
            LTR_Name = request.session['LTR_Name']
            LTR_Email = request.session['LTR_Email']
            Retention = config.O_DATA.format(
                f"/QYGMP?$filter=User_code%20eq%20%27{userID}%27")
            response = self.get_object(Retention)
            OpenProducts = [x for x in response['value']
                            if x['Status'] == 'Open']
            Pending = [x for x in response['value']
                       if x['Status'] == 'Processing']
            Approved = [x for x in response['value']
                        if x['Status'] == 'Approved']
            Rejected = [x for x in response['value']
                        if x['Status'] == 'Rejected']

            CountriesRegistered = config.O_DATA.format("/QYCountries")
            CountryResponse = self.get_object(CountriesRegistered)
            resCountry = CountryResponse['value']

        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect('gmp')
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect('login')
        openCount = len(OpenProducts)
        pendCount = len(Pending)
        appCount = len(Approved)
        rejectedCount = len(Rejected)
        ctx = {"openCount": openCount, "open": OpenProducts,
               "pendCount": pendCount, "pending": Pending, "appCount": appCount, "approved": Approved,
               "rejectedCount": rejectedCount, "rejected": Rejected,
               "country": resCountry, "LTR_Name": LTR_Name, "LTR_Email": LTR_Email}
        return render(request, 'gmp.html', ctx)

    def post(self, request):
        if request.method == "POST":
            try:
                gmpNo = request.POST.get('gmpNo')
                myAction = request.POST.get('myAction')
                userCode = request.session['UserID']
                typeOfManufacture = request.POST.get('typeOfManufacture')
                SitePhysicalAddress = request.POST.get('SitePhysicalAddress')
                SiteCountry = request.POST.get('SiteCountry')
                SiteTelephone = request.POST.get('SiteTelephone')
                SiteMobile = request.POST.get('SiteMobile')
                SiteEmail = request.POST.get('SiteEmail')
                isContact = eval(request.POST.get('isContact'))
                ContactName = request.POST.get('ContactName')
                ContactTel = request.POST.get('ContactTel')
                ContactEmail = request.POST.get('ContactEmail')
                previousGMPNo = request.POST.get('previousGMPNo')
                typeOfInspection = request.POST.get('typeOfInspection')
                stateOther = request.POST.get('StateOther')
                veterinaryPharmaceuticals = eval(request.POST.get(
                    'veterinaryPharmaceuticals'))
                poisons = eval(request.POST.get('poisons'))
                alternativeMedicines = eval(request.POST.get('alternativeMedicines'))
                biologicals = eval(request.POST.get('biologicals'))
                equipmentAndMaterials = eval(request.POST.get(
                    'equipmentAndMaterials'))
                nutrients = eval(request.POST.get('nutrients'))
                dosageForm = request.POST.get('dosageForm')
                productCategory = request.POST.get('productCategory')
                activity = request.POST.get('activity')
                iAgree = eval(request.POST.get('iAgree'))

                print(
                    gmpNo, myAction, userCode, typeOfManufacture, SitePhysicalAddress, SiteCountry, SiteTelephone, SiteMobile, SiteEmail, isContact, ContactName, ContactTel, ContactEmail, typeOfInspection, stateOther, veterinaryPharmaceuticals, poisons, alternativeMedicines, biologicals, equipmentAndMaterials, nutrients, dosageForm, productCategory, activity, iAgree, previousGMPNo
                )

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

                response = config.CLIENT.service.GMP(
                    gmpNo, myAction, userCode, typeOfManufacture, SitePhysicalAddress, SiteCountry, SiteTelephone, SiteMobile, SiteEmail, isContact, ContactName, ContactTel, ContactEmail, 
                    typeOfInspection, stateOther, veterinaryPharmaceuticals, poisons, alternativeMedicines, biologicals, equipmentAndMaterials, nutrients, dosageForm, productCategory, activity, iAgree,
                    previousGMPNo
                )
                print(response)
                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect('gmp')

            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('gmp')
            except KeyError as e:
                messages.info(request, "Session Expired, Login Again")
                print(e)
                return redirect('login')
        return redirect('gmp')


class GMPDetails(UserObjectMixin, View):
    def get(self, request, pk):
        print(pk)
        try:
            userID = request.session['UserID']
            LTR_Name = request.session['LTR_Name']
            LTR_Email = request.session['LTR_Email']
            Access_Point = config.O_DATA.format(
                f"/QYGMP?$filter=User_code%20eq%20%27{userID}%27%20and%20GMP_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']

            Lines = config.O_DATA.format(
                f"/QYLinestobeInspected?$filter=No%20eq%20%27{pk}%27%20and%20User_code%20eq%20%27{userID}%27")
            linesResponse = self.get_object(Lines)
            Line = [x for x in linesResponse['value']]

            ManufacturesParticulars = config.O_DATA.format(f"/QYGMPManufactureDetails?$filter=No%20eq%20%27{pk}%27")
            ManufacturerResponse = self.get_object(ManufacturesParticulars)
            Manufacturer = [x for x in ManufacturerResponse['value']]
            print(Manufacturer)

            Countries = config.O_DATA.format("/QYCountries")
            CountryResponse = self.get_object(Countries)
            resCountry = CountryResponse['value']

            Attachments = config.O_DATA.format("/QYGMPRequiredDocuments")
            AttachResponse = self.get_object(Attachments)
            attach = AttachResponse['value']

            AllAttachments = config.O_DATA.format(
                f"/QYDocumentAttachments?$filter=No_%20eq%20%27{pk}%27%20and%20Table_ID%20eq%2050004")
            AllAttachResponse = self.get_object(AllAttachments)
            Files = [x for x in AllAttachResponse['value']]

        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect('GMPDetails', pk=pk)
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect('login')

        ctx = {"res":responses,"status":Status,"line":Line,"manufacturer":Manufacturer,
        "country":resCountry,"files": Files,"attach":attach,"LTR_Name":LTR_Name,"LTR_Email":LTR_Email}
        return render(request,"gmpDetails.html",ctx)
    


def linesToInspect(request, pk):
    if request.method == "POST":
        try:
            myAction = request.POST.get('myAction')
            DosageForm = int(request.POST.get('DosageForm'))
            otherDosage = request.POST.get('otherDosage')
            Activity = int(request.POST.get('Activity'))
            lineNo = request.POST.get('lineNo')

            if not otherDosage:
                otherDosage = ''
            try:
                response = config.CLIENT.service.LinesInspected(pk, myAction, request.session['UserID'], DosageForm,
                                                                otherDosage, Activity, lineNo)
                print(response)
                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect('GMPDetails', pk=pk)
            except Exception as e:
                print(e)
                messages.error(request, e)
                return redirect('GMPDetails', pk=pk)
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect('GMPDetails', pk=pk)


class GMPGateway(UserObjectMixin, View):
    def get(self, request, pk):
        try:
            userID = request.session['UserID']
            LTR_Name = request.session['LTR_Name']
            LTR_Email = request.session['LTR_Email']
            Access_Point = config.O_DATA.format(
                f"/QYGMP?$filter=User_code%20eq%20%27{userID}%27%20and%20GMP_No_%20eq%20%27{pk}%27")
            response = self.get_object(Access_Point)
            for res in response['value']:
                responses = res
                Status = res['Status']
        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect('gmp')
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect('login')
        ctx = {"res": responses, "status": Status,
               "LTR_Name": LTR_Name, "LTR_Email": LTR_Email}
        return render(request, 'GMPGateway.html', ctx)

    def post(self, request, pk):
        if request.method == 'POST':
            try:
                transactionCode = request.POST.get('transactionCode')
                currency = request.POST.get('currency')

                if not transactionCode:
                    messages.error(request, "Transaction Code can't be empty.")
                    return redirect('GMPGateway', pk=pk)
                if not currency:
                    messages.error(
                        request, "Currency code missing please contact the system admin")
                    return redirect('GMPGateway', pk=pk)
                response = config.CLIENT.service.FnConfirmPayment(
                    transactionCode, currency, pk, request.session['UserID'])
                print(response)
                if response == True:
                    messages.success(
                        request, "Payment was successful. You can now submit your application.")
                    return redirect('GMPDetails', pk=pk)
                else:
                    messages.error("Payment Not sent. Try Again.")
                    return redirect('GMPGateway', pk=pk)
            except requests.exceptions.RequestException as e:
                messages.error(request, e)
                print(e)
                return redirect('GMPGateway', pk=pk)
            except KeyError as e:
                messages.info(request, "Session Expired, Login Again")
                print(e)
                return redirect('login')
            except Exception as e:
                messages.error(request, e)
                return redirect('GMPGateway', pk=pk)
        return redirect('GMPGateway', pk=pk)


def SubmitGMP(request, pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.SubmitGMP(
                pk, request.session['UserID'])
            print(response)
            if response == True:
                messages.success(request, "Document submitted successfully.")
                return redirect('GMPDetails', pk=pk)
            else:
                print("Not sent")
                return redirect('GMPDetails', pk=pk)
        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect('Registration')
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect('login')
        except Exception as e:
            messages.error(request, e)
            return redirect('GMPDetails', pk=pk)
    return redirect('GMPDetails', pk=pk)


def GMPManufactures(request, pk):
    if request.method == 'POST':
        try:
            gmpNo = pk
            myAction = request.POST.get('myAction')
            userId = request.session['UserID']
            manufacturerName = request.POST.get('manufacturerName')
            ManufacturerEmail = request.POST.get('ManufacturerEmail')
            postalAddress = request.POST.get('postalAddress')
            plantAddress = request.POST.get('plantAddress')
            ManufacturerTelephone = request.POST.get('ManufacturerTelephone')
            country = request.POST.get('country')
            activity = int(request.POST.get('activity'))
            TypeOfManufacturer = int(request.POST.get('TypeOfManufacturer'))
            manufacturerOther = request.POST.get('manufacturerOther')
            gmpMd = request.POST.get('gmpMd')
            if not manufacturerOther:
                manufacturerOther = ''
            try:
                response = config.CLIENT.service.GMPManufactureDetails(
                    gmpMd, myAction, userId,
                    manufacturerName, ManufacturerEmail, postalAddress, plantAddress, ManufacturerTelephone,
                    country, activity, TypeOfManufacturer, gmpNo
                )
                print(response)
                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect('GMPDetails', pk=pk)
                else:
                    print("Not sent")
                    return redirect('GMPDetails', pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect('GMPDetails', pk=pk)
            except Exception as e:
                messages.info(request, e)
                print(e)
                return redirect('GMPDetails', pk=pk)
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect('login')
    return redirect('GMPDetails', pk=pk)


def GMPAttachement(request, pk):
    if request.method == "POST":
        try:
            attach = request.FILES.get('attachment')
            filename = request.FILES['attachment'].name
            name = request.POST.get('name')
            tableID = 50004
            attachment = base64.b64encode(attach.read())

            try:
                response = config.CLIENT.service.GMPAttachement(
                    pk, filename, attachment, tableID, name)
                print(response)
                if response == True:
                    messages.success(request, "Upload Successful")
                    return redirect('GMPDetails', pk=pk)
                else:
                    messages.error(request, "Failed, Try Again")
                    return redirect('GMPDetails', pk=pk)
            except Exception as e:
                messages.error(request, e)
                print(e)
                return redirect('GMPDetails', pk=pk)
        except Exception as e:
            print(e)
    return redirect('GMPDetails', pk=pk)


def FnDeleteGMPDocumentAttachment(request, pk):
    if request.method == "POST":
        docID = int(request.POST.get('docID'))
        tableID = int(request.POST.get('tableID'))
        try:
            response = config.CLIENT.service.FnDeleteGMPDocumentAttachment(
                pk, docID, tableID)
            print(response)
            if response == True:
                messages.success(request, "Deleted Successfully ")
                return redirect('GMPDetails', pk=pk)
            else:
                messages.info(request, 'It is not Working')
        except Exception as e:
            messages.error(request, e)
            print(e)
    return redirect('GMPDetails', pk=pk)

def FNGenerateGMPInvoice(request, pk):
    if request.method == 'POST':
        try:
            response = config.CLIENT.service.FNGenerateGMPInvoice(pk)
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
    return redirect('GMPGateway', pk=pk)

    # To check against the user code to see whether there are products registered
