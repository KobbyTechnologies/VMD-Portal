import logging
from django.shortcuts import redirect, render
from django.conf import settings as config
import requests
from django.contrib import messages
import json
from datetime import datetime
import base64
import io as BytesIO
from django.http import HttpResponse
from django.views import View
from myRequest.views import UserObjectMixins
from django.http import JsonResponse

# Create your views here.


class UserObjectMixin(object):
    model = None
    session = requests.Session()
    session.auth = config.AUTHS

    def get_object(self, endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response


class registrationRequest(UserObjectMixin, View):
    def get(self, request):
        try:
            userId = request.session["UserID"]
            Vet_Classes = config.O_DATA.format("/QYVertinaryclasses")
            LTR_Name = request.session["LTR_Name"]
            LTR_Email = request.session["LTR_Email"]
            vet_response = self.get_object(Vet_Classes)
            product = vet_response["value"]

            Access_Point = config.O_DATA.format(
                f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27"
            )
            response = self.get_object(Access_Point)
            OpenProducts = [x for x in response["value"] if x["Status"] == "Open"]
            Pending = [x for x in response["value"] if x["Status"] == "Processing"]
            Approved = [x for x in response["value"] if x["Status"] == "Approved"]
            Rejected = [x for x in response["value"] if x["Status"] == "Rejected"]

            Country = config.O_DATA.format("/QYCountries")
            CountryResponse = self.get_object(Country)
            resCountry = CountryResponse["value"]

        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect("Registration")
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect("login")
        openCount = len(OpenProducts)
        pendCount = len(Pending)
        appCount = len(Approved)
        rejectedCount = len(Rejected)

        ctx = {
            "product": product,
            "openCount": openCount,
            "open": OpenProducts,
            "pendCount": pendCount,
            "pending": Pending,
            "appCount": appCount,
            "approved": Approved,
            "rejectedCount": rejectedCount,
            "rejected": Rejected,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
            "country": resCountry,
        }
        return render(request, "registration.html", ctx)


class myApplications(UserObjectMixin, View):
    def get(self, request, pk):
        try:
            userId = request.session["UserID"]
            LTR_Name = request.session["LTR_Name"]
            LTR_Email = request.session["LTR_Email"]
            Access_Point = config.O_DATA.format(
                f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27%20and%20ProductNo%20eq%20%27{pk}%27"
            )
            response = self.get_object(Access_Point)
            for res in response["value"]:
                responses = res
                Status = res["Status"]
                productClass = res["Veterinary_Classes"]

            Country = config.O_DATA.format("/QYCountries")
            CountryResponse = self.get_object(Country)
            resCountry = CountryResponse["value"]
        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect("applications")
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect("login")
        ctx = {
            "res": responses,
            "status": Status,
            "class": productClass,
            "country": resCountry,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
        }
        return render(request, "applications.html", ctx)


class filter_list(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            query = request.GET.get("query")
            user_id = request.session["UserID"]
            filter_one = request.GET.get("filter_one")
            filter_two = request.GET.get("filter_two")

            response = self.double_filtered_data(
                query, filter_one, "eq", pk, "and", filter_two, "eq", user_id
            )

            for response in response[1]:
                data = response
                return JsonResponse({"success": True, "data": data}, safe=False)
            return JsonResponse({"success": False, "error": "No Loan"})
        except Exception as e:
            logging.exception(e)
            return JsonResponse({"success": False, "error": e})


class ProductClass(UserObjectMixins, View):
    def post(self, request):
        try:
            vetClass = request.POST.get("vetClass")
            typeofManufacture = int(request.POST.get("typeofManufacture"))
            myAction = request.POST.get("myAction")
            userCode = request.session["UserID"]
            prodNo = request.POST.get("prodNo")
            if not prodNo:
                prodNo = ""
            response = self.make_soap_request(
                "FnClass", prodNo, vetClass, typeofManufacture, myAction, userCode
            )

            if response != "" and response != 0 and response != None:
                messages.success(request, f"Product {response} successfully created")
                return redirect("productDetails", pk=response)
            messages.error(request, f"{response}")
            return redirect("Registration")

        except Exception as e:
            messages.error(request, f"{e}")
            return redirect("Registration")


class productDetails(UserObjectMixin, View):
    def get(self, request, pk):
        try:
            UserID = request.session["UserID"]
            LTR_Name = request.session["LTR_Name"]
            LTR_Email = request.session["LTR_Email"]
            LTR_Country = request.session["Country"]
            LTR_BS_No = request.session["Business_Registration_No_"]
            userId = request.session["UserID"]
            Access_Point = config.O_DATA.format(
                f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27%20and%20ProductNo%20eq%20%27{pk}%27"
            )
            response = self.get_object(Access_Point)
            for res in response["value"]:
                responses = res
                Status = res["Status"]
                productClass = res["Veterinary_Classes"]

            Countries = config.O_DATA.format("/QYCountries")
            CountryResponse = self.get_object(Countries)
            resCountry = CountryResponse["value"]

            FeedAdditives = config.O_DATA.format(
                f"/QYAddictives?$filter=User_code%20eq%20%27{userId}%27%20and%20No%20eq%20%27{pk}%27"
            )
            AdditiveResponse = self.get_object(FeedAdditives)
            Additive = [x for x in AdditiveResponse["value"]]

            Methods = config.O_DATA.format(
                f"/QYMethods?$filter=User_Code%20eq%20%27{userId}%27%20and%20No%20eq%20%27{pk}%27"
            )
            MethodResponse = self.get_object(Methods)
            Method = [x for x in MethodResponse["value"]]

            Regulatories = config.O_DATA.format(
                f"/QyRegulatory?$filter%20=%20Usercode%20eq%20%27{userId}%27%20and%20ProductNo%20eq%20%27{pk}%27"
            )
            RegulatoryResponse = self.get_object(Regulatories)
            Regulatory = [x for x in RegulatoryResponse["value"]]
            # print(Regulatory)

            Attachments = config.O_DATA.format("/QYRequiredDocuments")
            AttachResponse = self.get_object(Attachments)
            attach = AttachResponse["value"]

            AllAttachments = config.O_DATA.format(
                f"/QYDocumentAttachments?$filter=No_%20eq%20%27{pk}%27%20and%20Table_ID%20eq%2052177996"
            )
            AllAttachResponse = self.get_object(AllAttachments)
            Files = [x for x in AllAttachResponse["value"]]

        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect("login")
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect("login")
        except Exception as e:
            messages.error(request, e)
            return redirect("login")

        ctx = {
            "res": responses,
            "status": Status,
            "class": productClass,
            "country": resCountry,
            "additive": Additive,
            "method": Method,
            "files": Files,
            "UserID": UserID,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
            "LTRBsNo": LTR_BS_No,
            "LTRCountry": LTR_Country,
            "attach": attach,
            "Regulatory": Regulatory,
        }

        return render(request, "productDetails.html", ctx)


class ManufacturesParticulars(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            Ingredients = self.one_filter(
                "/QYManufactureParticulers",
                "No",
                "eq",
                pk,
            )

            return JsonResponse(Ingredients, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)

    def post(self, request, pk):
        try:
            prodNo = pk
            myAction = request.POST.get("myAction")
            TypeOfManufacturer = int(request.POST.get("TypeOfManufacturer"))
            manufacturerOther = request.POST.get("manufacturerOther")
            manufacturerName = request.POST.get("manufacturerName")
            plantAddress = request.POST.get("plantAddress")
            country = request.POST.get("country")
            ManufacturerTelephone = request.POST.get("ManufacturerTelephone")
            ManufacturerEmail = request.POST.get("ManufacturerEmail")
            activity = int(request.POST.get("activity"))
            ManufacturerGMP = request.POST.get("ManufacturerGMP")
            userId = request.session["UserID"]
            lineNo = request.POST.get("lineNo")

            if not manufacturerOther:
                manufacturerOther = ""

            if not ManufacturerGMP:
                ManufacturerGMP = ""
            response = self.make_soap_request(
                "ManufacuresParticulars",
                prodNo,
                myAction,
                TypeOfManufacturer,
                manufacturerOther,
                manufacturerName,
                plantAddress,
                country,
                ManufacturerTelephone,
                ManufacturerEmail,
                activity,
                ManufacturerGMP,
                userId,
                lineNo,
            )
            if response == True:
                return JsonResponse({"success": True, "response": "Request successful"})
            else:
                return JsonResponse({"success": False, "error": response})

        except KeyError as e:
            return JsonResponse({"success": False, "error": str(e)})


class Ingredients(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            Ingredients = self.one_filter(
                "/QYIngredients",
                "No",
                "eq",
                pk,
            )

            return JsonResponse(Ingredients, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)

    def post(self, request, pk):
        try:
            prodNo = pk
            myAction = request.POST.get("myAction")
            ingredientType = request.POST.get("ingredientType")
            ingredientName = request.POST.get("ingredientName")
            quantityPerDose = request.POST.get("quantityPerDose")
            strengthOfIngredient = request.POST.get("strengthOfIngredient")
            Proportion = request.POST.get("Proportion")
            ReasonForInclusion = request.POST.get("ReasonForInclusion")
            specification = request.POST.get("specification")
            userId = request.session["UserID"]
            lineNo = request.POST.get("lineNo")
            if not ReasonForInclusion:
                ReasonForInclusion = ""

            response = self.make_soap_request(
                "Ingredients",
                prodNo,
                myAction,
                ingredientName,
                ingredientType,
                ReasonForInclusion,
                quantityPerDose,
                Proportion,
                specification,
                strengthOfIngredient,
                userId,
                lineNo,
            )
            if response == True:
                return JsonResponse({"success": True, "response": "Request successful"})
            else:
                return JsonResponse({"success": False, "error": response})

        except KeyError as e:
            return JsonResponse({"success": False, "error": str(e)})


class CountryRegistered(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            Countries = self.one_filter(
                "/QYCountriesRegistered",
                "No",
                "eq",
                pk,
            )

            return JsonResponse(Countries, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)

    def post(self, request, pk):
        try:
            prodNo = pk
            myAction = request.POST.get("myAction")
            country = request.POST.get("country")
            userId = request.session["UserID"]
            lineNo = request.POST.get("lineNo")

            response = self.make_soap_request(
                "CountriesRegistered", prodNo, myAction, country, userId, lineNo
            )
            if response == True:
                return JsonResponse({"success": True, "response": "Request successful"})
            else:
                return JsonResponse({"success": False, "error": response})

        except KeyError as e:
            return JsonResponse({"success": False, "error": str(e)})


class MarketingAuthorization(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            Marketing = self.one_filter(
                "/QYMarketingAuthorisation",
                "Country_No_",
                "eq",
                pk,
            )

            return JsonResponse(Marketing, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)

    def post(self, request, pk):
        try:
            myAction = request.POST.get("myAction")
            userId = request.session["UserID"]
            AuthorisationStatus = request.POST.get("AuthorisationStatus")
            MarketingCountry = request.POST.get("MarketingCountry")
            DateAuthorisation = datetime.strptime(
                request.POST.get("DateAuthorisation"), "%Y-%m-%d"
            ).date()
            AuthorisationNumber = request.POST.get("AuthorisationNumber")
            AuthorisationReason = request.POST.get("AuthorisationReason")
            ProprietaryName = request.POST.get("ProprietaryName")
            lineNo = request.POST.get("lineNo")

            if not AuthorisationReason:
                AuthorisationReason = ""
            if not AuthorisationNumber:
                AuthorisationNumber = ""
            if not ProprietaryName:
                ProprietaryName = ""
            response = self.make_soap_request(
                "MarketingAuthorisation",
                pk,
                myAction,
                userId,
                AuthorisationStatus,
                MarketingCountry,
                DateAuthorisation,
                AuthorisationNumber,
                AuthorisationReason,
                ProprietaryName,
                lineNo,
            )
            if response == True:
                return JsonResponse({"success": True, "response": "Request successful"})
            else:
                return JsonResponse({"success": False, "error": response})
        except KeyError as e:
            return JsonResponse({"success": False, "error": str(e)})


class makePayment(UserObjectMixin, View):
    def post(self, request, pk):
        if request.method == "POST":
            try:
                prodNo = pk
                userCode = request.session["UserID"]

                response = config.CLIENT.service.FnRegistrationPayment(prodNo, userCode)
                print(prodNo, userCode, response)
                if response == True:
                    messages.success(
                        request, "Please Make Your payment and click confirm payment."
                    )
                    return redirect("PaymentGateway", pk=pk)
                if response == False:
                    messages.error(request, "False")
                    return redirect("productDetails", pk=pk)
            except KeyError as e:
                messages.info(request, "Session Expired, Login Again")
                print(e)
                return redirect("login")
            except Exception as e:
                print(e)
                messages.info(request, e)
                return redirect("productDetails", pk=pk)
        return redirect("productDetails", pk=pk)


def SubmitRegistration(request, pk):
    if request.method == "POST":
        try:
            response = config.CLIENT.service.SubmitRegistration(
                pk, request.session["UserID"]
            )
            print(response)
            if response == True:
                messages.success(request, "Document submitted successfully.")
                return redirect("productDetails", pk=pk)
            else:
                print("Not sent")
                return redirect("productDetails", pk=pk)
        except requests.exceptions.RequestException as e:
            messages.error(request, e)
            print(e)
            return redirect("Registration")
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect("login")
        except Exception as e:
            messages.error(request, e)
            return redirect("productDetails", pk=pk)
    return redirect("productDetails", pk=pk)


class Attachments(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            Attachments = []
            attachURL = config.O_DATA.format(
                f"/QYDocumentAttachments?$filter=No_%20eq%20%27{pk}%27%20and%20Table_ID%20eq%2052177996"
            )
            response = self.get_object(attachURL)
            Attachments = [x for x in response["value"]]
            return JsonResponse(Attachments, safe=False)
        except Exception as e:
            logging.exception(e)
            return JsonResponse({"error": str(e)}, safe=False)

    def post(self, request, pk):
        try:
            attachment = request.FILES.get("attachment")
            if not attachment:
                return JsonResponse({"success": False, "error": "No attachment found"})

            file_extension = attachment.name.split(".")[-1]
            tableID = 52177996
            fileName = request.POST.get("attachmentCode") + "." + file_extension

            attachment_data = base64.b64encode(attachment.read())

            response = self.make_soap_request(
                "Attachement", pk, fileName, attachment_data, tableID
            )

            if response is not None:
                if response:
                    message = "Uploaded attachment successfully"
                    return JsonResponse({"success": True, "message": message})
                error = "Upload failed: {}".format(response)
                return JsonResponse({"success": False, "error": error})

            error = "Upload failed: Response from server was None"
            return JsonResponse({"success": False, "error": error})

        except Exception as e:
            error = "Upload failed: {}".format(e)
            logging.exception(e)
            return JsonResponse({"success": False, "error": error})


class DeleteAttachment(UserObjectMixins, View):
    def post(self, request):
        try:
            docID = int(request.POST.get("docID"))
            tableID = int(request.POST.get("tableID"))
            leaveCode = request.POST.get("leaveCode")
            response = self.make_soap_request(
                "FnDeleteDocumentAttachment", leaveCode, docID, tableID
            )
            if response == True:
                return JsonResponse(
                    {"success": True, "message": "Deleted successfully"}
                )
            return JsonResponse({"success": False, "message": f"{response}"})
        except Exception as e:
            error = "Upload failed: {}".format(e)
            logging.exception(e)
            return JsonResponse({"success": False, "error": error})


def GenerateCertificate(request, pk):
    if request.method == "POST":
        try:
            response = config.CLIENT.service.PrintCertificate(pk)
            buffer = BytesIO.BytesIO()
            content = base64.b64decode(response)
            buffer.write(content)
            responses = HttpResponse(
                buffer.getvalue(),
                content_type="application/pdf",
            )
            responses["Content-Disposition"] = f"inline;filename={pk}"
            return responses
        except Exception as e:
            messages.error(request, e)
            print(e)
    return redirect("productDetails", pk=pk)


def FnRegulatory(request, pk):
    if request.method == "POST":
        try:
            productNo = pk
            myAction = request.POST.get("myAction")
            userCode = request.session["UserID"]
            regulatory = request.POST.get("regulatory")
            regulatoryNo = request.POST.get("regulatoryNo")
            lineNo = request.POST.get("lineNo")

            if not lineNo:
                lineNo = ""

            try:
                response = config.CLIENT.service.FnRegulatory(
                    productNo, myAction, userCode, regulatory, regulatoryNo, lineNo
                )

                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect("productDetails", pk=pk)
                else:
                    print("Not sent")
                    return redirect("productDetails", pk=pk)
            except requests.exceptions.RequestException as e:
                print(e)
                return redirect("productDetails", pk=pk)
        except KeyError as e:
            messages.info(request, "Session Expired, Login Again")
            print(e)
            return redirect("login")
    return redirect("productDetails", pk=pk)
