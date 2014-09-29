from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from stackstreamer import settings
from stackorg.models import Stack

import os, os.path
import json
import hashlib

from django.contrib import messages

def login_user(request):
    if request.POST:
          username = request.POST.get('username')
          password = request.POST.get('password')

          user = authenticate(username=username, password=password)

          if user is not None:
              if user.is_active:
                  login(request, user)
                  return redirect('list_all_stacks')
              else:
                  # do something because user was not active
                  messages.add_message(request, messages.ERROR, 'User Inactive')
                  return render(request, 'login.html')
          else:
               # password/username combination was wrong
               messages.add_message(request, messages.ERROR, 'Invalid Credentials')
               return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login/")
def home(request):
    return redirect('list_all_stacks')

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