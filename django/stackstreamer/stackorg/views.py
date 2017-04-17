from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required

from stackstreamer import settings
from stackorg.models import Stack, Project

from exportroi.models import DataExport
from scripts.cmdline import cmd_import_data

import os, os.path
import json
import hashlib

def datalist(request):
    dns = os.listdir(settings.DATA_PATH)
    dns = [dn for dn in dns if os.path.isdir(settings.DATA_PATH+dn)]
    html = "<html><body>It is now %s.</body></html>" % repr(dns)
    return HttpResponse(html)

def import_stacks(request):
    cmd_import_data()
    return redirect('list_all_stacks')

@login_required
def list_all_stacks(request):
    stacks = Stack.objects.all()
    # View code here...
    return render(request, 'list.html', {"stacks": stacks}, 
        content_type="text/html")

@login_required
def list_all_projects(request):
    projects = Project.objects.all()
    for p in projects:
        p.nstacks = len(Stack.objects.filter(project=p.id))
    # View code here...
    return render(request, 'projectlist.html', {"projects": projects}, 
        content_type="text/html")

@login_required
def list_exports(request, stackid):
    stack = Stack.objects.get(pk=stackid)
    exports = DataExport.objects.filter(stack=stackid)
    # View code here...
    return render(request, 'exportlist.html', {"stack": stack, "exports":exports}, 
        content_type="text/html")    

@login_required
def list_project_stacks(request, projectid):
    p = Project.objects.get(pk=projectid)
    stacks = Stack.objects.filter(project=p)
    # View code here...
    return render(request, 'list.html', {"stacks": stacks}, 
        content_type="text/html")
  
