from django.contrib import messages
from django.shortcuts import render,redirect

# Create your views here.
def sidebar(request):
    return render(request, "sidebar.html")
def profileRequest(request):
    try:
        userID = request.session['UserID']
        LTR_Name = request.session['LTR_Name']
        LTR_Email = request.session['LTR_Email']
        Country = request.session['Country']
        Business_Registration_No_= request.session['Business_Registration_No_']
    except KeyError as e:
        messages.error(request,e) 
        return redirect('login')
    ctx = {"userID":userID,"LTR_Name":LTR_Name,"Country":Country,"LTR_Email":LTR_Email,
        "Business_Registration_No_":Business_Registration_No_}
    return render(request,'profile.html',ctx)
def contact(request):
    return render(request,'contact.html')

def FAQRequest(request):
    try:
        LTR_Name = request.session['LTR_Name']
        LTR_Email = request.session['LTR_Email']
    except KeyError as e:
        messages.error(request,e) 
        return redirect('login')
    ctx = {"LTR_Name":LTR_Name,"LTR_Email":LTR_Email}
    return render(request,'faq.html',ctx)

def Manual(request):
    try:
        LTR_Name = request.session['LTR_Name']
        LTR_Email = request.session['LTR_Email']
    except KeyError as e:
        messages.error(request,e) 
        return redirect('login')
    ctx = {"LTR_Name":LTR_Name,"LTR_Email":LTR_Email}
    return render(request,'manual.html',ctx)