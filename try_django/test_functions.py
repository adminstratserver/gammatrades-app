from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
import os
from dotenv import load_dotenv
load_dotenv()

def test_printdata(request):
    current_site = get_current_site(request)
    #print('1. current_site=', current_site)
    #print('2. current_site.domain=', current_site.domain)
    return HttpResponse('email Send from GammaTrades email')
    #return HttpResponse('current site:', current_site, current_site.domain)

def test_mail(request):
    send_mail('Test Email', 'Test message sent on 6th August 9:12am', 'admin@gammatrades.net', ['cryptocoinwiz@gmail.com','heydudde@gmail.com'])
    return HttpResponse('email Send from GammaTrades email')

def test_getenviron(request):
    sendgridapi1 = os.environ.get('SENDGRID_API_KEY')
    awskeyid1 = os.environ.get('AWS_ACCESS_KEY_ID')
    awsaccesskey1 = os.environ.get('AWS_SECRET_ACCESS_KEY')
    awss3bucket1 = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    secretkey1 = os.environ.get('SECRET_KEY')

    sqlengine1 = os.environ.get('SQL_ENGINE')
    sqldb1 = os.environ.get('SQL_DATABASE')
    sqluser1 = os.environ.get('SQL_USER')
    sqlpassword1 = os.environ.get('SQL_PASSWORD')
    sqlhost1 = os.environ.get('SQL_HOST')
    sqlport1 = os.environ.get('SQL_PORT')
    sqldebug1 = os.environ.get('DEBUG')

    #print('sendgridapi1=', sendgridapi1)
    #print('awskeyid1=', awskeyid1)
    #print('awsaccesskey1=', awsaccesskey1)
    #print('awss3bucket1=', awss3bucket1)
    #print('secretkey1=', secretkey1)

    #print('sqlengine1=', sqlengine1)
    #print('sqldb1=', sqldb1)
    #print('sqluser1=', sqluser1)
    #print('sqlpassword1=', sqlpassword1)
    #print('sqlhost1=', sqlhost1)
    #print('sqlport1=', sqlport1)
    #print('sqldebug1=', sqldebug1)





    return HttpResponse('ok done!')