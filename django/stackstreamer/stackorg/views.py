from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required

from stackstreamer import settings
from stackorg.models import Stack

from exportroi.models import DataExport

import os, os.path
import json
import hashlib

def datalist(request):
    dns = os.listdir(settings.DATA_PATH)
    dns = [dn for dn in dns if os.path.isdir(settings.DATA_PATH+dn)]
    html = "<html><body>It is now %s.</body></html>" % repr(dns)
    return HttpResponse(html)

@login_required
def list_all_stacks(request):
    stacks = Stack.objects.all()
    # View code here...
    return render(request, 'list.html', {"stacks": stacks, 'VIEWER_URL':settings.VIEWER_URL}, 
        content_type="text/html")


@login_required
def list_exports(request, stackid):
    stack = Stack.objects.get(pk=stackid)
    exports = DataExport.objects.filter(stack=stackid)
    # View code here...
    return render(request, 'exportlist.html', {"stack": stack, "exports":exports, 'VIEWER_URL':settings.VIEWER_URL}, 
        content_type="text/html")    