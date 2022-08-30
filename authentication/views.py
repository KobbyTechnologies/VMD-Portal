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

def get_object(endpoint):
    session = requests.Session()
    session.auth = config.AUTHS
    response = session.get(endpoint, timeout=10).json()
    return response

def passwordCipher(password):
    Portal_Password = base64.urlsafe_b64decode(password)
    cipher_suite = Fernet(config.ENCRYPT_KEY)
    decoded_text = cipher_suite.decrypt(Portal_Password).decode("ascii")
    return decoded_text


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_reset_mail(email,request):
    current_site = get_current_site(request)
    email_subject = 'Reset Your Password'
    email_body = render_to_string('resetMail.html',{
        'domain': current_site
    })
    reset_email = EmailMessage(subject=email_subject,body=email_body,from_email=config.EMAIL_HOST_USER,to=[email])

    EmailThread(reset_email).start()

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
    Access_Point = config.O_DATA.format("/QYCountries")
    try:
        response = get_object(Access_Point)
        resCountry = response['value']
    except requests.exceptions.RequestException as e:
        print(e)
        return redirect('register')
    ctx = {"country":resCountry}
    return render(request,"register.html",ctx)

def registerAccount(request):

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
            myAction = "insert"
        
            if len(Password) < 6:
                messages.error(request, "Password should be at least 6 characters")
                return redirect('register')
            if Password != Password2:
                messages.error(request, "Password mismatch")
                return redirect('register')
            nameChars = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                            for i in range(5))
            verificationToken = str(nameChars)

            myPassword = passwordCipher(Password)

            response = config.CLIENT.service.FnRegistrationSignup(lTRName, lTRMail, countryRegionCode,postalAddress,postCode,businessRegNo,city,myPassword,verificationToken, myAction)
            print(response)
            if response == True:
                send_mail(lTRMail,verificationToken,request)
                messages.success(
                request, 'We sent you an email to verify your account')
                return redirect('login')
            messages.info(request,"Email not Sent, Try with Signing up with another email")
            return redirect('register')
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
            Access_Point = config.O_DATA.format(f"/QYLTRLogins?$filter=LTR_Email%20eq%20%27{email}%27")
            response = get_object(Access_Point)
            for res in response['value']:
                if res['Verification_Token'] == secret:
                    response = config.CLIENT.service.FnVerified(verified, email)
                    messages.success(request,"Verification Successful")
                    return redirect('login')
        except requests.exceptions.RequestException as e:
            print(e)
            messages.error(request,"Not Verified. check Credentials or Register")
            return redirect('verify')
        except ValueError:
            messages.error(request,'Wrong Input')
            return redirect('verify')
    return render(request,"verify.html")

def loginRequest(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            Access_Point = config.O_DATA.format(f"/QYLTRLogins?$filter=LTR_Email%20eq%20%27{email}%27")
            response = get_object(Access_Point)            
            for res in response['value']:
                if res['Verified'] == True:
                    request.session['UserID'] = res['No']
                    request.session['LTR_Name'] = res['LTR_Name']
                    request.session['LTR_Email'] = res['LTR_Email']
                    request.session['Country'] = res['Country']
                    request.session['Business_Registration_No_'] = res['Business_Registration_No_']
                    decoded_text = passwordCipher(res['MyPassword'])
                    if decoded_text == password:
                        print("User ID:",request.session['UserID'] )
                        return redirect('dashboard')
                    else:
                        messages.error(request, "Invalid Password")
                        return redirect('login')
        except requests.exceptions.RequestException as e:
            print(e)
            messages.error(request,e)
            return redirect('login')
        except ValueError:
            messages.error(request,'Missing Input')
            return redirect('login')
    return render(request,'login.html') 

def resetPassword(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
        except  ValueError:
            messages.error(request,'Missing Input')
            return redirect('login')
        session = requests.Session()
        session.auth = config.AUTHS
        Access_Point = config.O_DATA.format("/QYLTRLogins")
        try:
            response = session.get(Access_Point, timeout=10).json()
            for res in response['value']:
                try:
                    if res['LTR_Email'] == email:
                        request.session['resetMail'] = email
                        send_reset_mail(email,request)
                        messages.success(request, 'We sent you an email to reset your password')
                        return redirect('login')
                    else:
                        messages.error(request,"Invalid Email")
                        return redirect('login')
                except:
                    messages.error(request,"Invalid Email")
                    return redirect('login')
        except Exception as e:
            messages.error(request, e)
            print(e)
            return redirect('login')       
    return redirect("login")

def reset_request(request):
    if request.method == 'POST':
        try:
            email = request.session['resetMail']
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            verified = True
        except KeyError:
            messages.info(request,"Session Expired, Raise new password reset request")
            return redirect('login')
        except  ValueError:
            messages.error(request,'Invalid Input')
            return redirect('reset')
        if len(password) < 6:
            messages.error(request, "Password should be at least 6 characters")
            return redirect('reset')
        if password != password2:
            messages.error(request, "Password mismatch")
            return redirect('reset')   
        cipher_suite = Fernet(config.ENCRYPT_KEY)
        encrypted_text = cipher_suite.encrypt(password.encode('ascii'))
        myPassword = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
        try:
            response = config.CLIENT.service.FnResetPassword(email, myPassword,verified)
            print(response)
            if response == True:
                messages.success(request,"Reset successful")
                del request.session['resetMail']
                return redirect('login')
            else:
                messages.error(request,"Error Try Again")
                return redirect('reset')
        except Exception as e:
            messages.error(request, e)
            print(e)
            return redirect('reset')
    return render(request,'reset.html')
def logout_request(request):
    try:
        del request.session['UserID'] 
        del request.session['LTR_Name']
        del request.session['LTR_Email']
        del request.session['Country']
        del request.session['Business_Registration_No_'] 
    except Exception as e:
        messages.info(request,e)
        return redirect ('login')
    return redirect('login')