from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings as config
from django.contrib import messages
import requests
from myRequest.views import UserObjectMixins
from django.views import View


# Create your views here.
class VeterinaryPharmaceutical(UserObjectMixins, View):
    def post(self, request, pk):
        try:
            myAction = "modify"
            prodName = request.POST.get("prodName")
            packSize = request.POST.get("packSize")
            PharmaceuticalDosage = request.POST.get("PharmaceuticalDosage")
            RouteOfAdministration = request.POST.get("RouteOfAdministration")
            shelfLifeAfterDilution = request.POST.get("shelfLifeAfterDilution")
            shelfLifeAfterFirstOpening = request.POST.get("shelfLifeAfterFirstOpening")
            storageConditions = request.POST.get("storageConditions")
            storageAfterOpening = request.POST.get("storageAfterOpening")
            PharmacotherapeuticGroup = request.POST.get("PharmacotherapeuticGroup")
            ATCCode = request.POST.get("ATCCode")
            controlledVeterinaryMedicine = request.POST.get(
                "controlledVeterinaryMedicine"
            )
            prescriptionOnlyMedicine = request.POST.get("prescriptionOnlyMedicine")
            nonPharmacy = request.POST.get("nonPharmacy")
            pharmaciesOnly = request.POST.get("pharmaciesOnly")
            iAgree = eval(request.POST.get("iAgree"))
            userId = request.session["UserID"]
            CountryOfOrigin = request.POST.get("CountryOfOrigin")
            CountryOfRelease = request.POST.get("CountryOfRelease")
            signatoryName = request.POST.get("signatoryName")
            signatoryPosition = request.POST.get("signatoryPosition")
            companyName = request.POST.get("companyName")
            companyAddress = request.POST.get("companyAddress")
            CountryOrigin = request.POST.get("CountryOrigin")
            companyTel = request.POST.get("companyTel")
            companyFax = request.POST.get("companyFax")
            companyEmail = request.POST.get("companyEmail")
            mainIndication = request.POST.get("mainIndication")
            descriptionOfProduct = request.POST.get("descriptionOfProduct")

            if not iAgree:
                iAgree = False
            if not controlledVeterinaryMedicine:
                controlledVeterinaryMedicine = "False"
            if not prescriptionOnlyMedicine:
                prescriptionOnlyMedicine = "False"
            if not nonPharmacy:
                nonPharmacy = "False"
            if not pharmaciesOnly:
                pharmaciesOnly = "False"
            if not ATCCode:
                messages.info(
                    request, "You must have an ATC Code to register a product"
                )
                return redirect("registration")

            nonPharmacy = eval(nonPharmacy)
            pharmaciesOnly = eval(pharmaciesOnly)
            controlledVeterinaryMedicine = eval(controlledVeterinaryMedicine)

            response = self.make_soap_request(
                "FnPharmaceuticalCard",
                pk,
                myAction,
                prodName,
                packSize,
                PharmaceuticalDosage,
                RouteOfAdministration,
                shelfLifeAfterDilution,
                shelfLifeAfterFirstOpening,
                storageConditions,
                storageAfterOpening,
                PharmacotherapeuticGroup,
                ATCCode,
                controlledVeterinaryMedicine,
                prescriptionOnlyMedicine,
                nonPharmacy,
                pharmaciesOnly,
                userId,
                CountryOfOrigin,
                CountryOfRelease,
                iAgree,
                signatoryName,
                signatoryPosition,
                companyName,
                companyAddress,
                CountryOrigin,
                companyTel,
                companyFax,
                companyEmail,
                mainIndication,
                descriptionOfProduct,
            )
            if response == True:
                return JsonResponse({"success": True, "response": "Request successful"})
            else:
                return JsonResponse({"success": False, "error": response})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
