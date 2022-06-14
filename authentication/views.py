from django.shortcuts import render,redirect
import requests
from django.conf import settings as config
from django.contrib import messages
import secrets
import string
from cryptography.fernet import Fernet
import base64
from django.contrib.sites.shortcuts import get_current_site
from  django.template.loader import render_to_string
from django.core.mail import EmailMessage
import threading

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_mail(lTRMail,verificationToken,request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'
    email_body = render_to_string('activate.html',{
        'domain': current_site,
        'Secret': verificationToken,
    })

    email = EmailMessage(subject=email_subject,body=email_body,from_email=config.EMAIL_HOST_USER,to=[lTRMail])

    EmailThread(email).start()

# Register View
def registerRequest(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/QYCountries")
    try:
        response = session.get(Access_Point, timeout=10).json()
        resCountry = response['value']
    except requests.exceptions.RequestException as e:
        print(e)
    ctx = {"country":resCountry}
    return render(request,"register.html",ctx)

def registerAccount(request):
    lTRName = ""
    lTRMail = ""
    countryRegionCode = ""
    postalAddress = ""
    postCode = ""
    businessRegNo = ""
    city = ""
    myPassword = ""
    verificationToken = ""
    myAction = "insert"

    if request.method == 'POST':
        try:
            lTRName = request.POST.get('lTRName')
            lTRMail = request.POST.get('lTRMail')
            countryRegionCode = request.POST.get('countryRegionCode')
            postalAddress = request.POST.get('postalAddress')
            postCode = request.POST.get('postCode')
            businessRegNo = request.POST.get('businessRegNo')
            city = request.POST.get('city')
            Password = request.POST.get('Password')
            Password2 = request.POST.get('Password2')
        except ValueError:
            messages.error(request, "Not sent. Invalid Input, Try Again!!")
            return redirect('register')
        if len(Password) < 6:
            messages.error(request, "Password should be at least 6 characters")
            return redirect('register')
        if Password != Password2:
            messages.error(request, "Password mismatch")
            return redirect('register')
        nameChars = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                        for i in range(5))
        verificationToken = str(nameChars)

        cipher_suite = Fernet(config.ENCRYPT_KEY)
        encrypted_text = cipher_suite.encrypt(Password.encode('ascii'))
        myPassword = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        print(myPassword)
        try:
            response = config.CLIENT.service.FnRegistrationSignup(lTRName, lTRMail, countryRegionCode,postalAddress,postCode,businessRegNo,city,myPassword,verificationToken, myAction)
            print(response)
            if response == True:
                try:
                    send_mail(lTRMail,verificationToken,request)
                    messages.success(
                    request, 'We sent you an email to verify your account')
                    request.session['prospectEmail'] = lTRMail
                except:
                    messages.info(request,"Email not Sent, Try with Signing up with another email")
                    return redirect('register')
            return redirect('login')
        except Exception as e:
            messages.error(request, e)
            print(e)
            return redirect('register')
    return redirect('register')

def loginRequest(request):
    return render(request,'reset.html')       

# Login View
def verifyRequest(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            secret = request.POST.get('secret')
            verified = True
        except ValueError:
            messages.error(request,'Wrong Input')
            return redirect('verify')
        session = requests.Session()
        session.auth = config.AUTHS
        Access_Point = config.O_DATA.format("/QYLTRLogins")
        try:
            response = session.get(Access_Point, timeout=10).json()
            for res in response['value']:
                if res['LTR_Email'] == email and res['Verification_Token'] == secret:
                    try:
                        response = config.CLIENT.service.FnVerified(verified, email)
                        messages.success(request,"Verification Successful")
                        return redirect('login')
                    except requests.exceptions.RequestException as e:
                        messages.error(request,e)
                        print(e)
                        return redirect('verify')
        except requests.exceptions.RequestException as e:
            print(e)
            messages.error(request,"Not Verified. check Credentials or Register")
            return redirect('verify')
    return render(request,"verify.html")

def loginRequest(request):
    return render(request,'login.html') 