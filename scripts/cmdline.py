from stackstreamer import settings
from stackstreamer.prettyprint import *
import os, os.path, sys

def cmd_list_data():
    dns = os.listdir(settings.DATA_PATH)
    dns = [dn for dn in dns if os.path.isdir(settings.DATA_PATH+dn)]
    print(dns)

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