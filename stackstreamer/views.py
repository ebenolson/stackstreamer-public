from django.shortcuts import render
from stackstreamer import settings
# Create your views here.
from django.http import HttpResponse
import os, os.path

def home(request):
    html = "<html><body>Welcome to StackStreamer</body></html>"
    return HttpResponse(html)