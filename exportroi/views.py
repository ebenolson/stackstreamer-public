from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required

from stackstreamer import settings
from stackstreamer.prettyprint import *

import exportroi.export

import os, os.path
import json
import hashlib

@login_required
def export_full_slice(request, uuid, slice):
   # View code here...
   print uuid, slice
   fn = exportroi.export.export_full_slice(uuid, int(slice))
   dbg(fn)
   print(fn)
   return redirect(fn)