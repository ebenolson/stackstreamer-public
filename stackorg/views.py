from django.shortcuts import render
from stackstreamer import settings
from stackorg.models import Stack
# Create your views here.
from django.http import HttpResponse
import os, os.path
from django.contrib.auth.decorators import login_required

def datalist(request):
    dns = os.listdir(settings.DATA_PATH)
    dns = [dn for dn in dns if os.path.isdir(settings.DATA_PATH+dn)]
    html = "<html><body>It is now %s.</body></html>" % repr(dns)
    return HttpResponse(html)

@login_required
def list_all_stacks(request):
    stacks = Stack.objects.all()
    # View code here...
    return render(request, 'list.html', {"stacks": stacks}, 
        content_type="application/xhtml+xml")