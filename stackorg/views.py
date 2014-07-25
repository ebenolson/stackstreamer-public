from django.shortcuts import render
from stackstreamer import settings
# Create your views here.
from django.http import HttpResponse
import os, os.path

def datalist(request):
    dns = os.listdir(settings.DATA_PATH)
    dns = [dn for dn in dns if os.path.isdir(settings.DATA_PATH+dn)]
    html = "<html><body>It is now %s.</body></html>" % repr(dns)
    return HttpResponse(html)