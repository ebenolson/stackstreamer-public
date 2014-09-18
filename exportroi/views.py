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

@login_required
def export_snapshot(request, uuid, slice, zoom, x0, y0, x1, y1):
    # View code here...
    try:
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)
        zoom = int(zoom)
        slice = int(slice)
    except ValueError:
        return HttpResponse(status=400)

    fn = exportroi.export.export_snapshot(uuid, slice, zoom, x0, y0, x1, y1)
    dbg(fn)
    print(fn)
    if not fn:
        return HttpResponse(status=400)
    else:
        return redirect(settings.MEDIA_URL+fn)
