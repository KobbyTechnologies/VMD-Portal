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
                task_get_inspection = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QyWholesaleInspection", "UserCode", "eq", userID
                    )
                )

                response = await asyncio.gather(
                    task_get_permits, task_get_countries, task_get_inspection
                )

                permits = [x for x in response[0]]
                Approved = [x for x in response[0] if x["Status"] == "Approved"]

                resCountry = [x for x in response[1]]
                Approved_Inspection = [
                    x for x in response[2] if x["Status"] == "Approved"
                ]

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
            "Approved_Inspection": Approved_Inspection,
        }
        return render(request, "permit.html", ctx)

    async def post(self, request):
        try:
            premiseNo = request.POST.get("premiseNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            inspectionNo = request.POST.get("inspectionNo")
            premiseName = request.POST.get("premiseName")
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

            if not inspectionNo:
                inspectionNo = "None"

            response = self.make_soap_request(
                "FnWholesalePremisePermit",
                premiseNo,
                userCode,
                premiseName,
                inspectionNo,
                building,
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
                        session,
                        "/QyWholesalePremisePermit",
                        "PremiseNo",
                        "eq",
                        pk,
                    )
                )
                task_get_inspection = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QyWholesaleInspection", "UserCode", "eq", userID
                    )
                )
                task_get_countries = asyncio.ensure_future(
                    self.simple_fetch_data(session, "/QYCountries")
                )
                response = await asyncio.gather(
                    task_get_permit, task_get_countries, task_get_inspection
                )
                for permit in response[0]:
                    if permit["UserCode"] == userID:
                        permit = permit
                resCountry = [x for x in response[1]]
                Approved_Inspection = [
                    x for x in response[2] if x["Status"] == "Approved"
                ]
        except Exception as e:
            messages.info(request, f"{e}")
            print(e)
            return redirect("dashboard")
        ctx = {
            "permit": permit,
            "country": resCountry,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
            "Approved_Inspection": Approved_Inspection,
        }
        return render(request, "permit-detail.html", ctx)

    async def post(self, request, pk):
        try:
            myAction = request.POST.get("myAction")
            lineNo = request.POST.get("lineNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            pro_name = request.POST.get("pro_name")
            position_in_business = request.POST.get("position_in_business")
            professionalRegNo = request.POST.get("professionalRegNo")
            qualificationAndExperience = request.POST.get("qualificationAndExperience")
            nationality = request.POST.get("nationality")
            iDorPassportOrAlienIDNo = request.POST.get("iDorPassportOrAlienIDNo")

            response = self.make_soap_request(
                "FnWholesalePremiseLine",
                pk,
                myAction,
                lineNo,
                pro_name,
                position_in_business,
                qualificationAndExperience,
                iDorPassportOrAlienIDNo,
                nationality,
                professionalRegNo,
                userCode,
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


class Customer(UserObjectMixins, View):
    async def post(self, request):
        try:
            premiseNo = request.POST.get("premiseNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")

            response = self.make_soap_request(
                "FnWholesalePremisePermitPayment",
                premiseNo,
                userCode,
            )
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                if response == True:
                    return JsonResponse({"response": str(response)}, safe=False)
                return JsonResponse({"error": str(response)}, safe=False)
            else:
                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect("PermitDetails", pk=premiseNo)
                else:
                    messages.error(request, f"{response}")
                    return redirect("PermitDetails", pk=premiseNo)
        except Exception as e:
            logging.exception(e)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"error": str(e)}, safe=False)
            else:
                messages.error(request, f"{e}")
                return redirect("PermitDetails", pk=premiseNo)


class FNGenerateInvoice(UserObjectMixins, View):
    def post(self, request):
        try:
            premiseNo = request.POST.get("premiseNo")
            filenameFromApp = "invoice_" + premiseNo + ".pdf"
            response = self.make_soap_request(
                "FNGenerateWholesalePremiseInvoice", premiseNo
            )

            buffer = BytesIO.BytesIO()
            content = base64.b64decode(response)
            buffer.write(content)
            responses = HttpResponse(
                buffer.getvalue(),
                content_type="application/pdf",
            )
            responses["Content-Disposition"] = f"inline;filename={filenameFromApp}"
            return responses
        except Exception as e:
            messages.error(request, f"Failed, {e}")
            logging.exception(e)
            return redirect("PermitDetails", pk=premiseNo)


class PermitAttachments(UserObjectMixins, View):
    async def get(self, request, pk):
        try:
            Attachments = []
            async with aiohttp.ClientSession() as session:
                task_get_attachments = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QYDocumentAttachments", "No_", "eq", pk
                    )
                )
                response = await asyncio.gather(task_get_attachments)

                Attachments = [x for x in response[0]]
                return JsonResponse(Attachments, safe=False)

        except Exception as e:
            logging.exception(e)
            return JsonResponse({"error": str(e)}, safe=False)

    async def post(self, request, pk):
        try:
            attachments = request.FILES.getlist("attachment")
            tableID = 50040
            attachment_names = []
            response = False
            for file in attachments:
                fileName = file.name
                attachment_names.append(fileName)
                attachment = base64.b64encode(file.read())
                response = self.make_soap_request(
                    "FnAttachementWholesalePremisePermit",
                    pk,
                    fileName,
                    attachment,
                    tableID,
                )
            if response is not None:
                if response == True:
                    message = "Uploaded {} attachments successfully".format(
                        len(attachments)
                    )
                    return JsonResponse({"success": True, "message": message})
                error = "Upload failed: {}".format(response)
                return JsonResponse({"success": False, "error": error})
            error = "Upload failed: Response from server was None"
            return JsonResponse({"success": False, "error": error})
        except Exception as e:
            error = "Upload failed: {}".format(e)
            logging.exception(e)
            return JsonResponse({"success": False, "error": error})


class RemovePermitAttachment(UserObjectMixins, View):
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


class SubmitWholesalePermit(UserObjectMixins, View):
    def post(self, request, pk):
        try:
            userCode = request.session["UserID"]

            response = self.make_soap_request("SubmitWholesalePermit", pk, userCode)

            if response == True:
                return JsonResponse({"response": str(response)}, safe=False)
            return JsonResponse({"error": str(response)}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)


class PremiseCert(UserObjectMixins, View):
    def post(self, request, pk):
        try:
            filenameFromApp = "Premise_Cert_" + pk + ".pdf"
            response = self.make_soap_request(
                "PrintWholesalePremisePermitCertificate", pk
            )
            buffer = BytesIO.BytesIO()
            content = base64.b64decode(response)
            buffer.write(content)
            responses = HttpResponse(
                buffer.getvalue(),
                content_type="application/pdf",
            )
            responses["Content-Disposition"] = f"inline;filename={filenameFromApp}"
            return responses
        except Exception as e:
            messages.error(request, f"Failed, {e}")
            logging.exception(e)
            return redirect("PermitDetails", pk=pk)


#
# QyAdvertisement
# QyManufacturingLicence
# QyManufacturingLicenceLines
# QyInspectorateRequiredDocument
