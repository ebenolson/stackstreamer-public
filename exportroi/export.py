from stackstreamer import settings
from stackstreamer.prettyprint import *
from stackorg.models import Stack
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files import File
from django.core.files.base import ContentFile
from cStringIO import StringIO
from PIL import Image
import numpy as np

import os, os.path, sys
import json, uuid

def export_full_slice(uuid, slice):
    try:
        stack = Stack.objects.get(uuid=uuid)
    except ObjectDoesNotExist, MultipleObjectsReturned:
        return False

    if slice > stack.n_slices-1:
        return False

    try:
        stack_info = json.load(open(stack.path+'/info.json'))
    except:
        return False

    ts = [t for t in stack_info['tile sets'] if t['zoom'] == 0]
    if len(ts) == 1:
        ts = ts[0]
        pixel_width = ts['nx']*stack_info['tile size']
        pixel_height = ts['ny']*stack_info['tile size']
    else:
        return False

    TS = int(stack_info['tile size'])

    oim = np.zeros((pixel_height, pixel_width, 3),dtype='uint8')
    
    for i in range(ts['nx']):
        for j in range(ts['ny']):
            im = Image.open(stack.path+'/pyramid/channel1/zoom0/slice_%04d/tile_x%04d_y%04d.80.jpg'%(slice, i, j))
            oim[j*TS:(j+1)*TS, i*TS:(i+1)*TS, :] = np.array(im)

    fn = settings.MEDIA_ROOT+'/export/%s_layer_%04d.png'%(uuid,slice)
    Image.fromarray(oim).save(fn)
    return fn
