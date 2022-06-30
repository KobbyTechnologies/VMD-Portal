from django.shortcuts import render,redirect
from django.conf import settings as config
from django.contrib import messages
import requests
import  json
from newsapi import NewsApiClient
from datetime import date

# Create your views here.
def dashboard(request):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point= config.O_DATA.format("/QYRegistration")
    newsapi = NewsApiClient(api_key='5c2c534258a44addb5e6cfd97db6e9ce')
    today = date.today()
    OpenProducts = []
    Pending = []
    Approved = []
    Rejected =[]
    try:
        response = session.get(Access_Point, timeout=10).json()
        for res in response['value']:
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Open':
                output_json = json.dumps(res)
                OpenProducts.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Pending Approval':
                output_json = json.dumps(res)
                Pending.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Approved':
                output_json = json.dumps(res)
                Approved.append(json.loads(output_json))
            if res['User_code'] == request.session['UserID'] and res['Status'] == 'Rejected':
                output_json = json.dumps(res)
                Rejected.append(json.loads(output_json))
    
        all_articles = newsapi.get_everything(q='nairobi',
                                      sources='abc-news',
                                      from_param=f'{today}',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='publishedAt',
                                      page=2)

        articles = all_articles['articles']
    except requests.exceptions.RequestException as e:
        messages.error(request,e)
        print(e)
        return redirect('dashboard')
    except KeyError as e:
        messages.info(request,"Session Expired, Login Again")
        print(e)
        return redirect('login')
    openCount = len(OpenProducts)
    pendCount = len(Pending)
    appCount = len(Approved)
    rejectedCount = len(Rejected)
    ctx = {"openCount":openCount,"open":OpenProducts,
    "pendCount":pendCount,"pending":Pending,"appCount":appCount,"approved":Approved,
    "rejectedCount":rejectedCount,"rejected":Rejected,"articles":articles}
    return render (request,"dashboard.html",ctx)
