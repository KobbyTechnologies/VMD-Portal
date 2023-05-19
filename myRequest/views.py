from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import requests
from django.conf import settings as config
import datetime as dt
from requests.auth import HTTPBasicAuth
from zeep.client import Client
from zeep.transports import Transport
from requests import Session
from django.http import HttpResponseRedirect
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import secrets
import string
from cryptography.fernet import Fernet
import base64
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import date
from django.core.mail import EmailMessage
import datetime as dt
import threading

session = None


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


# Create your views here.
class UserObjectMixins(object):
    model = None
    sessions = requests.Session()
    sessions.auth = config.AUTHS
    todays_date = dt.datetime.now().strftime("%b. %d, %Y %A")
    cipher_suite = Fernet(config.ENCRYPT_KEY)
    O_DATA_AUTH = aiohttp.BasicAuth(config.WEB_SERVICE_UID, config.WEB_SERVICE_PWD)

    def verificationToken(self, tokenRange):
        alphabet = string.ascii_letters + string.digits
        SecretCode = "".join(secrets.choice(alphabet) for i in range(tokenRange))
        return SecretCode

    def pass_encrypt(self, password):
        encrypted_text = self.cipher_suite.encrypt(password.encode("ascii"))
        encrypted_password = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_password

    def pass_decrypt(self, password):
        Portal_Password = base64.urlsafe_b64decode(password)
        decoded_text = self.cipher_suite.decrypt(Portal_Password).decode("ascii")
        return decoded_text

    def send_mail(self, request, subject, template, recipient, recipient_email, token):
        current_site = get_current_site(request)
        email_body = render_to_string(
            template,
            {
                "user": recipient,
                "domain": current_site,
                "Secret": token,
            },
        )
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=config.EMAIL_HOST_USER,
            to=[recipient_email],
        )
        email.content_subtype = "html"
        EmailThread(email).start()
        return True

    def send_message(
        self, name, reply_email, subject, message, email_template, recipient_email
    ):
        email_body = render_to_string(
            email_template,
            {
                "user": name,
                "message": message,
            },
        )
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=config.EMAIL_HOST_USER,
            to=[recipient_email],
            reply_to=[reply_email],
        )
        email.content_subtype = "html"
        EmailThread(email).start()
        return True

    async def fetch_data(self, session, username, password, endpoint, property, filter):
        auth = aiohttp.BasicAuth(login=username, password=password)
        async with session.get(
            config.O_DATA.format(
                f"{endpoint}?$filter={property}%20{filter}%20%27{username}%27"
            ),
            auth=auth,
        ) as res:
            data = await res.json()
            response = {"status_code": res.status, "data": data["value"]}
            return response

    async def simple_fetch_data(self, session, endpoint):
        async with session.get(
            config.O_DATA.format(endpoint), auth=self.O_DATA_AUTH
        ) as res:
            data = await res.json()
            response = data["value"]
            return response

    async def fetch_one_filtered_data(
        self, session, endpoint, property, filter, field_name
    ):
        async with session.get(
            config.O_DATA.format(
                f"{endpoint}?$filter={property}%20{filter}%20%27{field_name}%27"
            ),
            auth=self.O_DATA_AUTH,
        ) as res:
            data = await res.json()
            response = {"status_code": res.status, "data": data["value"]}
            return response

    async def simple_one_filtered_data(
        self, session, endpoint, property, filter, field_name
    ):
        async with session.get(
            config.O_DATA.format(
                f"{endpoint}?$filter={property}%20{filter}%20%27{field_name}%27"
            ),
            auth=self.O_DATA_AUTH,
        ) as res:
            data = await res.json()
            response = data["value"]
            return response

    async def simple_double_filtered_data(
        self,
        session,
        endpoint,
        property_x,
        filter_x,
        filed_name_x,
        operater_1,
        property_y,
        filter_y,
        field_name_y,
    ):
        async with session.get(
            config.O_DATA.format(
                f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{filed_name_x}%27%20{operater_1}%20{property_y}%20{filter_y}%20%27{field_name_y}%27"
            ),
            auth=self.O_DATA_AUTH,
        ) as res:
            data = await res.json()
            response = data["value"]
            return response

    def make_soap_request(self, endpoint, *params):
        global session
        if not session:
            session = Session()
            session.auth = HTTPBasicAuth(config.WEB_SERVICE_UID, config.WEB_SERVICE_PWD)
        with ThreadPoolExecutor() as executor:
            client = Client(config.BASE_URL, transport=Transport(session=session))
            response = executor.submit(client.service[endpoint], *params).result()
        return response

    def upload_attachment(self, *params):
        global session
        if not session:
            session = Session()
            session.auth = HTTPBasicAuth(config.WEB_SERVICE_UID, config.WEB_SERVICE_PWD)
        with ThreadPoolExecutor() as executor:
            client = Client(self.WEB_PORTAL, transport=Transport(session=session))
            response = executor.submit(
                client.service["FnUploadAttachedDocument"], *params
            ).result()
        return response

    def delete_attachment(self, *params):
        global session
        if not session:
            session = Session()
            session.auth = HTTPBasicAuth(config.WEB_SERVICE_UID, config.WEB_SERVICE_PWD)
        with ThreadPoolExecutor() as executor:
            client = Client(self.WEB_PORTAL, transport=Transport(session=session))
            response = executor.submit(
                client.service["FnDeleteDocumentAttachment"], *params
            ).result()
        return response

    def download_attachment(self, *params):
        global session
        if not session:
            session = Session()
            session.auth = HTTPBasicAuth(config.WEB_SERVICE_UID, config.WEB_SERVICE_PWD)
        with ThreadPoolExecutor() as executor:
            client = Client(self.WEB_PORTAL, transport=Transport(session=session))
            response = executor.submit(
                client.service["FnGetDocumentAttachment"], *params
            ).result()
        return response

    def get_object(self, endpoint):
        response = self.sessions.get(endpoint).json()
        return response

    def one_filter(self, endpoint, property, filter, field_name):
        Access_Point = config.O_DATA.format(
            f"{endpoint}?$filter={property}%20{filter}%20%27{field_name}%27"
        )
        response = self.get_object(Access_Point)["value"]
        count = len(response)
        return count, response

    def double_filtered_data(
        self,
        endpoint,
        property_x,
        filter_x,
        filed_name_x,
        operater_1,
        property_y,
        filter_y,
        field_name_y,
    ):
        Access_Point = config.O_DATA.format(
            f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{filed_name_x}%27%20{operater_1}%20{property_y}%20{filter_y}%20%27{field_name_y}%27"
        )
        response = self.get_object(Access_Point)["value"]
        count = len(response)
        return count, response

    def triple_filtered_data(
        self,
        endpoint,
        property_x,
        filter_x,
        filed_name_x,
        operater_1,
        property_y,
        filter_y,
        field_name_y,
        operater_2,
        property_z,
        filter_z,
        field_name_z,
    ):
        Access_Point = config.O_DATA.format(
            f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{filed_name_x}%27%20{operater_1}%20{property_y}%20{filter_y}%20%27{field_name_y}%27%20{operater_2}%20{property_z}%20{filter_z}%20%27{field_name_z}%27"
        )
        response = self.get_object(Access_Point)["value"]
        count = len(response)
        return count, response

    def zeep_client(self, request):
        Username = request.session["User_ID"]
        Password = request.session["password"]
        AUTHS = Session()
        AUTHS.auth = HTTPBasicAuth(Username, Password)
        CLIENT = Client(config.BASE_URL, transport=Transport(session=AUTHS))
        return CLIENT

    def comparison_double_filter(
        self,
        endpoint,
        property_x,
        filter_x,
        field_name,
        operater_1,
        property_y,
        filter_y,
        property_z,
    ):
        Access_Point = config.O_DATA.format(
            f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{field_name}%27%20{operater_1}%20{property_y}%20{filter_y}%20{property_z}"
        )
        response = self.get_object(Access_Point)["value"]
        count = len(response)
        return count, response

    def quotes(self):
        category = "health"
        QUOTES_API_KEY = "EIvOjryX23PBwPSqeoWNbA==52tdKajnJVd8uImQ"
        api_url = "https://api.api-ninjas.com/v1/quotes?category={}".format(category)
        try:
            response = requests.get(api_url, headers={"X-Api-Key": QUOTES_API_KEY})
            if response.status_code == requests.codes.ok:
                return response.json()
        except Exception as e:
            return None


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]

    status_code = 200
