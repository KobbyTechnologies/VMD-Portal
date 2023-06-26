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
class Advertisement(UserObjectMixins, View):
    async def get(self, request):
        try:
            userID = await sync_to_async(request.session.__getitem__)("UserID")
            LTR_Name = await sync_to_async(request.session.__getitem__)("LTR_Name")
            LTR_Email = await sync_to_async(request.session.__getitem__)("LTR_Email")

            async with aiohttp.ClientSession() as session:
                task = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QyAdvertisement", "UserCode", "eq", userID
                    )
                )
                task_get_countries = asyncio.ensure_future(
                    self.simple_fetch_data(session, "/QYCountries")
                )

                response = await asyncio.gather(task, task_get_countries)

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
        return render(request, "advertise.html", ctx)

    async def post(self, request):
        try:
            advertisementNo = request.POST.get("advertisementNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            countryOfManufacture = request.POST.get("countryOfManufacture")
            formOfAdvertisement = request.POST.get("formOfAdvertisement")
            myAction = request.POST.get("myAction")

            response = self.make_soap_request(
                "FnAdvartisementCard",
                advertisementNo,
                countryOfManufacture,
                formOfAdvertisement,
                userCode,
                myAction,
            )
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                if response != None and response != "" and response != 0:
                    return JsonResponse({"response": str(response)}, safe=False)
                return JsonResponse({"error": str(response)}, safe=False)
            else:
                if response != "0" and response is not None and response != "":
                    messages.success(request, "Request Successful")
                    return redirect("AdvertiseDetails", pk=response)
                else:
                    messages.error(request, f"{response}")
                    return redirect("advertise")
        except Exception as e:
            logging.exception(e)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"error": str(e)}, safe=False)
            else:
                messages.error(request, f"{e}")
                return redirect("advertise")


class AdvertiseDetails(UserObjectMixins, View):
    async def get(self, request, pk):
        try:
            userID = await sync_to_async(request.session.__getitem__)("UserID")
            LTR_Name = await sync_to_async(request.session.__getitem__)("LTR_Name")
            LTR_Email = await sync_to_async(request.session.__getitem__)("LTR_Email")
            res = {}

            async with aiohttp.ClientSession() as session:
                task = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QyAdvertisement", "AdvartisementNo", "eq", pk
                    )
                )
                task_get_countries = asyncio.ensure_future(
                    self.simple_fetch_data(session, "/QYCountries")
                )
                response = await asyncio.gather(task, task_get_countries)
                for task in response[0]:
                    if task["UserCode"] == userID:
                        res = task
                resCountry = [x for x in response[1]]
        except Exception as e:
            messages.info(request, f"{e}")
            print(e)
            return redirect("dashboard")
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            return JsonResponse(res, safe=False)

        ctx = {
            "permit": res,
            "country": resCountry,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
        }
        return render(request, "advertise-detail.html", ctx)

    async def post(self, request, pk):
        try:
            lineNo = request.POST.get("lineNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            pro_name = request.POST.get("pro_name")
            marketingAuthorizationNo = request.POST.get("marketingAuthorizationNo")
            formulation = request.POST.get("formulation")
            category = int(request.POST.get("category"))
            targetAudience = request.POST.get("targetAudience")
            uses = request.POST.get("uses")
            countryOfManufacture = request.POST.get("countryOfManufacture")
            myAction = request.POST.get("myAction")

            response = self.make_soap_request(
                "FnAdvartisementLines",
                pk,
                lineNo,
                pro_name,
                marketingAuthorizationNo,
                formulation,
                category,
                targetAudience,
                uses,
                countryOfManufacture,
                userCode,
                myAction,
            )
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


class AdvertisementLines(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            PermitLines = self.one_filter(
                "/QyAdvertisementLines",
                "AdvartisementNo",
                "eq",
                pk,
            )

            return JsonResponse(PermitLines, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)
