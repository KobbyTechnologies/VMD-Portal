import base64
import logging
from django.shortcuts import render, redirect
from django.conf import settings as config
from django.contrib import messages
from django.views import View
import io as BytesIO
from django.http import HttpResponse, JsonResponse
from myRequest.views import UserObjectMixins
from asgiref.sync import sync_to_async
import asyncio
import aiohttp
from datetime import datetime


# Create your views here.
class ManufacturingLicense(UserObjectMixins, View):
    async def get(self, request):
        try:
            userID = await sync_to_async(request.session.__getitem__)("UserID")
            LTR_Name = await sync_to_async(request.session.__getitem__)("LTR_Name")
            LTR_Email = await sync_to_async(request.session.__getitem__)("LTR_Email")

            async with aiohttp.ClientSession() as session:
                task_get_permits = asyncio.ensure_future(
                    self.simple_one_filtered_data(
                        session, "/QyManufacturingLicence", "UserCode", "eq", userID
                    )
                )

                response = await asyncio.gather(task_get_permits)

                permits = [x for x in response[0]]
                Approved = [x for x in response[0] if x["Status"] == "Approved"]

        except Exception as e:
            messages.info(request, f"{e}")
            print(e)
            return redirect("dashboard")
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            return JsonResponse(permits, safe=False)

        ctx = {
            "approved": Approved,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
        }
        return render(request, "manufacture.html", ctx)

    async def post(self, request):
        try:
            manufacturingNo = request.POST.get("manufacturingNo")
            gMPStandards = request.POST.get("gMPStandards")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            date = "2023-07-09"
            iAgree = eval(request.POST.get("iAgree"))
            myAction = request.POST.get("myAction")
            if not iAgree:
                iAgree = False

            defaultDate = datetime.strptime((date), "%Y-%m-%d").date()

            response = self.make_soap_request(
                "FnManufacturingLicenceCard",
                manufacturingNo,
                gMPStandards,
                defaultDate,
                iAgree,
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
                    return redirect("ManufacturingLicenseDetails", pk=response)
                else:
                    messages.error(request, f"{response}")
                    return redirect("ManufacturingLicense")
        except Exception as e:
            logging.exception(e)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"error": str(e)}, safe=False)
            else:
                messages.error(request, f"{e}")
                return redirect("ManufacturingLicense")


class ManufacturingLicenseDetails(UserObjectMixins, View):
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
                        "/QyManufacturingLicence",
                        "ManufacturingNo",
                        "eq",
                        pk,
                    )
                )
                response = await asyncio.gather(task_get_permit)
                for permit in response[0]:
                    if permit["UserCode"] == userID:
                        permit = permit
        except Exception as e:
            messages.info(request, f"{e}")
            print(e)
            return redirect("dashboard")
        ctx = {
            "permit": permit,
            "LTR_Name": LTR_Name,
            "LTR_Email": LTR_Email,
        }
        return render(request, "manufacture-detail.html", ctx)

    async def post(self, request, pk):
        try:
            myAction = request.POST.get("myAction")
            lineNo = request.POST.get("lineNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")
            veterinaryMedicineName = request.POST.get("veterinaryMedicineName")
            medicineComposition = request.POST.get("medicineComposition")
            directPersonalSupervisor = request.POST.get("directPersonalSupervisor")
            supervisorQualifications = request.POST.get("supervisorQualifications")

            response = self.make_soap_request(
                "FnManufacturingLcenecLines",
                pk,
                lineNo,
                veterinaryMedicineName,
                medicineComposition,
                directPersonalSupervisor,
                supervisorQualifications,
                userCode,
                myAction,
            )
            print(response)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                if response == True:
                    return JsonResponse({"response": str(response)}, safe=False)
                return JsonResponse({"error": str(response)}, safe=False)
            else:
                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect("ManufacturingLicenseDetails", pk=pk)
                else:
                    messages.error(request, f"{response}")
                    return redirect("ManufacturingLicenseDetails", pk=pk)
        except Exception as e:
            logging.exception(e)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"error": str(e)}, safe=False)
            else:
                messages.error(request, f"{e}")
                return redirect("ManufacturingLicenseDetails", pk=pk)


class ManufacturingLicenseLines(UserObjectMixins, View):
    def get(self, request, pk):
        try:
            PermitLines = self.one_filter(
                "/QyManufacturingLicenceLines",
                "ManufacturingNo",
                "eq",
                pk,
            )

            return JsonResponse(PermitLines, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)


class ManufacturingLicenseCustomer(UserObjectMixins, View):
    async def post(self, request):
        try:
            manufacturingNo = request.POST.get("manufacturingNo")
            userCode = await sync_to_async(request.session.__getitem__)("UserID")

            response = self.make_soap_request(
                "FnManufacturingLicencePayment",
                manufacturingNo,
                userCode,
            )
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                if response == True:
                    return JsonResponse({"response": str(response)}, safe=False)
                return JsonResponse({"error": str(response)}, safe=False)
            else:
                if response == True:
                    messages.success(request, "Request Successful")
                    return redirect("ManufacturingLicenseDetails", pk=manufacturingNo)
                else:
                    messages.error(request, f"{response}")
                    return redirect("ManufacturingLicenseDetails", pk=manufacturingNo)
        except Exception as e:
            logging.exception(e)
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"error": str(e)}, safe=False)
            else:
                messages.error(request, f"{e}")
                return redirect("ManufacturingLicenseDetails", pk=manufacturingNo)


class ManufacturingLicenseInvoice(UserObjectMixins, View):
    def post(self, request):
        try:
            manufacturingNo = request.POST.get("manufacturingNo")
            filenameFromApp = "invoice_" + manufacturingNo + ".pdf"
            response = self.make_soap_request(
                "FNGenerateManufacturingLicenceInvoice", manufacturingNo
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
            return redirect("ManufacturingLicenseDetails", pk=manufacturingNo)


class ManufacturingLicenseAttachments(UserObjectMixins, View):
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
                    "FnAttachementManufacturingLicence",
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


class SubmitManufacturingLicense(UserObjectMixins, View):
    def post(self, request, pk):
        try:
            userCode = request.session["UserID"]

            response = self.make_soap_request(
                "SubmitManufacturingLicence", pk, userCode
            )

            if response == True:
                return JsonResponse({"response": str(response)}, safe=False)
            return JsonResponse({"error": str(response)}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, safe=False)


class ManufacturingLicenseCert(UserObjectMixins, View):
    def post(self, request, pk):
        try:
            filenameFromApp = "Manufacturing_License_Cert_" + pk + ".pdf"
            response = self.make_soap_request(
                "PrintManufacturingLicenceCertificate", pk
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
            return redirect("ManufacturingLicenseDetails", pk=pk)
