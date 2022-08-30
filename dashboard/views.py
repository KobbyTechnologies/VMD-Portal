from django.shortcuts import render,redirect
from django.conf import settings as config
from django.contrib import messages
import requests
import  json
from newsapi import NewsApiClient
from datetime import date

def get_object(endpoint):
    session = requests.Session()
    session.auth = config.AUTHS
    response = session.get(endpoint, timeout=10).json()
    return response

# Create your views here.
def dashboard(request):
    try:
        userId = request.session['UserID']
        Access_Point= config.O_DATA.format(f"/QYRegistration?$filter=User_code%20eq%20%27{userId}%27")
        response = get_object(Access_Point)

        OpenProducts = [x for x in response['value'] if x['Status'] == 'Open']
        Pending = [x for x in response['value'] if x['Status'] == 'Processing']
        Approved = [x for x in response['value'] if x['Approval_Status'] == 'Approved']
        Rejected = [x for x in response['value'] if x['Approval_Status'] == 'Disapproved']

        newsapi = NewsApiClient(api_key='5c2c534258a44addb5e6cfd97db6e9ce')
        today = date.today()
    
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
