from __future__ import print_function
import os

COLORS = {'blue':'94m', 'cyan':'36m', 'green':'92m', 'grey':'30m', 
          'magenta':'95m', 'red':'31m', 'white':'37m', 'yellow':'33m',
          'darkblue':'34m', 'darkpink':'35m', 'lightred':'91m', 'lightyellow':'93m', 'darkgreen':'32m', 'lightcyan':'96m',
          'reset':'0m'}
PREFIX= '\033['
RESET = PREFIX+'0m'

def calc_colors_enabled():
    e = os.getenv('ANSI_COLORS_DISABLED')
    #return 'COLORTERM' in os.environ and (e is None or e == '0' or e.lower() == 'false')
    return (e is None or e == '0' or e.lower() == 'false')
color_enabled = calc_colors_enabled()

def colorize(txt, color):
    if color_enabled and color and color in COLORS:
        return ''.join([PREFIX,COLORS[color],txt,RESET])
    else:
        return txt

def switch_color(color_name):
    if color_enabled:
        print(PREFIX+COLORS[color_name],end='')

def print_colored(*args, **kwargs):
    #import traceback
    #traceback.print_stack()
    if not args:
        print()
        return
    color = kwargs.get('color')
    prefix = kwargs.get('prefix')
    if kwargs.get('no_prefix', None): prefix = None
    if args and args[0] and isinstance(args[0],basestring) and args[0][0] == '\n':
        prefix = None
    if color_enabled and color and color in COLORS:
        print(PREFIX+COLORS[color],end='')
        if prefix is not None:
            print(_to_unicode(prefix),end=' ')
        for a in args:
            print(_to_unicode(a),end=' ')
        print(RESET, end=kwargs.get('end','\n'))
    else:
        if prefix is not None:
            print(_to_unicode(prefix),end=' ')
        for a in args:
            print(_to_unicode(a),end=' ')
        print(end=kwargs.get('end','\n'))

def print_regular(*args, **kwargs):
    if not args:
        print()
        return
    prefix = kwargs['prefix'] if 'prefix' in kwargs else None
    if kwargs.get('no_prefix', None): prefix = None
    if prefix is not None:
        print(_to_unicode(prefix),end=' ')
    for a in args:
        print(_to_unicode(a),end=' ')
    print()

def _to_unicode(a):
    return unicode(a).encode('utf-8','ignore')

def printf(*args, **kwargs):
    print_regular(*args, **kwargs)

def err(*args, **kwargs):
    print_colored(color='red', *args, **kwargs)

def info(*args, **kwargs):
    print_colored(color='green', *args, **kwargs)

def dbg(*args, **kwargs):
    print_colored(color='blue', *args, **kwargs)

def warn(*args, **kwargs):
    print_colored(color='yellow', *args, **kwargs)

