from stackstreamer import settings
from stackstreamer.prettyprint import *
from stackorg.models import Stack
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files import File
from django.core.files.base import ContentFile
from cStringIO import StringIO
from PIL import Image

import os, os.path, sys
import json, uuid

def cmd_list_data():
    dns = os.listdir(settings.DATA_PATH)
    dns = [settings.DATA_PATH+dn for dn in dns if os.path.isdir(settings.DATA_PATH+dn)]
    print(dns)

def cmd_import_data(update=False):
    dns = os.listdir(settings.DATA_PATH)
    dns = [settings.DATA_PATH+dn for dn in dns if os.path.isdir(settings.DATA_PATH+dn)]    

    for dn in dns:
        dbg(dn)
        try:
	    stack_info = json.load(open(dn+'/info.json'))
        except:
            continue	
        if 'uuid' not in stack_info:
            info('adding uuid')
            stack_info['uuid'] = str(uuid.uuid4())
            json.dump(stack_info, open(dn+'/info.json','w'))

        try:
            obj = Stack.objects.get(uuid=stack_info['uuid'])
            if not update:
                continue
            dbg('Updating Stack')

        except ObjectDoesNotExist:
            obj = Stack()
            dbg('Importing new Stack')
            obj.uuid = stack_info['uuid']

        except MultipleObjectsReturned:
            error('Multiple entries for %s with uuid %s' % (dn, info['uuid']) )
            continue

        obj.path = dn
        obj.name = dn.split('/')[-1]
        obj.pixel_size = stack_info['pixel size']
        obj.slice_spacing = stack_info['slice spacing']
        ts = [t for t in stack_info['tile sets'] if t['zoom'] == 0]
        if len(ts) == 1:
            ts = ts[0]
            obj.pixel_width = ts['nx']*stack_info['tile size']
            obj.pixel_height = ts['ny']*stack_info['tile size']
        obj.n_slices = stack_info['number of slices']

        pil_image_obj = Image.open(dn+'/thumb.png')
        f = StringIO()
        try:
            pil_image_obj.save(f, format='png')
            s = f.getvalue()
            obj.thumbnail.save('/thumbnails/'+obj.uuid+'.png', ContentFile(s))
            warn('/thumbnails/'+obj.uuid+'.png')
        finally:
            f.close()

        obj.save()

def usage():
	print('python -m scripts.cmdline <command_name>')

def main():
    if '--help' in ' '.join(sys.argv):
        usage()
        exit(0)
        
    if len(sys.argv) > 1:
        func_name = sys.argv[1]
        
        if func_name in ('id', 'long'): func_name = '_'+func_name
        func = globals().get('cmd_'+func_name if not func_name.startswith('cmd_') else func_name)
        
        if not func:
            err('No function named "%s"' % func_name)
            exit(1)
        
        args = []
        kwargs = {}
        for arg in sys.argv[2:]:
            if '=' in arg and arg.startswith('--'):
                k,v = arg.split('=',1)
                while k[0] == '-':
                    k = k[1:]
                k = k.replace('-','_')
                kwargs[k] = v
            else:
                args.append(arg)
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            info('Cancelled by user')
    
    info('DONE')

if __name__ == '__main__':
    main()
