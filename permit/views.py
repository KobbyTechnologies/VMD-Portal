import base64
import logging
from django.shortcuts import render, redirect
import requests
import json
from django.conf import settings as config
from django.contrib import messages
from django.views import View
import io as BytesIO
from django.http import HttpResponse, JsonResponse
from myRequest.views import UserObjectMixins
from asgiref.sync import sync_to_async
import asyncio
import aiohttp


# Create your views here.
class Permit(UserObjectMixins, View):
    async def get(self, request):
        try:
            userID = await sync_to_async(request.session.__getitem__)("UserID")
            LTR_Name = await sync_to_async(request.session.__getitem__)("LTR_Name")
            LTR_Email = await sync_to_async(request.session.__getitem__)("LTR_Email")

            async with aiohttp.ClientSession() as session:
                task_get_permits = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QyWholesalePremisePermit", "UserCode", "eq", userID
                    )
                )
                task_get_countries = asyncio.ensure_future(
                    self.simple_fetch_data(session, "/QYCountries")
                )

                response = await asyncio.gather(task_get_permits, task_get_countries)

                permits = [x for x in response[0]]
                Approved = [x for x in response[0] if x["Status"] == "Approved"]

                resCountry = [x for x in response[1]]

        except Exception as e:
            messages.info(request, f"{e}")
            print(e)
            return redirect("dashboard")
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            return JsonResponse(permits, safe=False)

        ctx = {
            "approved": Approved,
            "country": resCountry,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
        }
        return render(request, "permit.html", ctx)

    async def post(self, request):
        try:
            premiseNo = request.POST.get("premiseNo")
            professionalRegNo = request.POST.get("professionalRegNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            iDorPassportOrAlienIDNo = request.POST.get("iDorPassportOrAlienIDNo")
            nationality = request.POST.get("nationality")
            premiseName = request.POST.get("premiseName")
            qualification = request.POST.get("qualification")
            periodOfExperience = request.POST.get("periodOfExperience")
            premiseLocation = request.POST.get("premiseLocation")
            town = request.POST.get("town")
            road = request.POST.get("road")
            building = request.POST.get("building")
            applicantName = request.POST.get("applicantName")
            plotNo = request.POST.get("plotNo")
            firstTimeApplication = int(request.POST.get("firstTimeApplication"))
            iAgree = eval(request.POST.get("iAgree"))
            myAction = request.POST.get("myAction")
            if not iAgree:
                iAgree = False

            response = self.make_soap_request(
                "FnWholesalePremisePermit",
                premiseNo,
                professionalRegNo,
                userCode,
                iDorPassportOrAlienIDNo,
                nationality,
                premiseName,
                qualification,
                periodOfExperience,
                premiseLocation,
                town,
                road,
                building,
                applicantName,
                plotNo,
                firstTimeApplication,
                iAgree,
                myAction,
            )
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                if response != None and response != "" and response != 0:
                    return JsonResponse({"response": str(response)}, safe=False)
                return JsonResponse({"error": str(response)}, safe=False)
            else:
                if response != "0" and response is not None and response != "":
                    messages.success(request, "Request Successful")
                    return redirect("PermitDetails", pk=response)
                else:
                    messages.error(request, f"{response}")
                    return redirect("permit")
        except Exception as e:
            logging.exception(e)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"error": str(e)}, safe=False)
            else:
                messages.error(request, f"{e}")
                return redirect("permit")


class PermitDetails(UserObjectMixins, View):
    async def get(self, request, pk):
        try:
            userID = await sync_to_async(request.session.__getitem__)("UserID")
            LTR_Name = await sync_to_async(request.session.__getitem__)("LTR_Name")
            LTR_Email = await sync_to_async(request.session.__getitem__)("LTR_Email")
            permit = {}

            async with aiohttp.ClientSession() as session:
                task_get_permit = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QyWholesalePremisePermit", "PremiseNo", "eq", pk
                    )
                )
                task_get_countries = asyncio.ensure_future(
                    self.simple_fetch_data(session, "/QYCountries")
                )
                response = await asyncio.gather(task_get_permit, task_get_countries)
                for permit in response[0]:
                    if permit["UserCode"] == userID:
                        permit = permit
                resCountry = [x for x in response[1]]
        except Exception as e:
            messages.info(request, f"{e}")
            print(e)
            return redirect("dashboard")
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            return JsonResponse(permit, safe=False)

        ctx = {
            "permit": permit,
            "country": resCountry,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
        }
        return render(request, "permit-detail.html", ctx)

    async def post(self, request, pk):
        try:
            myAction = request.POST.get("myAction")
            lineNo = request.POST.get("lineNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            pro_name = request.POST.get("pro_name")
            position_in_business = request.POST.get("position_in_business")
            reg_no = request.POST.get("reg_no")
            qualificationAndExperience = request.POST.get("qualificationAndExperience")

            response = self.make_soap_request(
                "FnWholesalePremiseLine",
                pk,
                myAction,
                lineNo,
                pro_name,
                position_in_business,
                reg_no,
                qualificationAndExperience,
                userCode,
            )
            print(response)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                if response == True:
                    return JsonResponse({"response": str(response)}, safe=False)
                return JsonResponse({"error": str(response)}, safe=False)
            else:
                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect("PermitDetails", pk=pk)
                else:
                    messages.error(request, f"{response}")
                    return redirect("PermitDetails", pk=pk)
        except Exception as e:
            logging.exception(e)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"error": str(e)}, safe=False)
            else:
                messages.error(request, f"{e}")
                return redirect("PermitDetails", pk=pk)


class Professionals(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            PermitLines = self.one_filter(
                "/QyWholesalePremisePermitLines",
                "PremiseNo",
                "eq",
                pk,
            )

            return JsonResponse(PermitLines, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)


# QyWholesalePremisePermit
#
# QyRetailDealersPremisePermit
# QyRetailDealersPremiseLines
# QyAdvertisement
# QyManufacturingLicence
# QyManufacturingLicenceLines
# QyInspectorateRequiredDocument
