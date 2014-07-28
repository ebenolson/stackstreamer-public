from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required

from stackstreamer import settings
from stackorg.models import Stack

import os, os.path
import json
import hashlib

def home(request):
    html = "<html><body>Welcome to StackStreamer</body></html>"
    return HttpResponse(html)


def get_stack_data_path(request, uuid):
    response_data = {}

    response_data['uuid'] = uuid
#    uuid = request.GET.get('uuid', '')
    try:
        stack = Stack.objects.get(uuid=uuid)
        response_data['result'] = 'success'
        response_data['path'] = stack.path

    except ObjectDoesNotExist, MultipleObjectsReturned:
        response_data['result'] = 'failed'
        response_data['path'] = ''

    return HttpResponse(json.dumps(response_data), content_type="application/json")    

def verify_access_token(request, access_token, response_token):
    response_data = {}

    response_data['result'] = 'success'
    response_data['signed token'] = hashlib.sha256(access_token+response_token+settings.VIEWER_SECRET_KEY).hexdigest()
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")    