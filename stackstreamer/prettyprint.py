import print_helper
print_prefix = ''

def err(*args, **kwargs):          print_helper.err(prefix=print_prefix+' Error:', *args, **kwargs)
def info(*args, **kwargs):         print_helper.info(prefix=print_prefix, *args, **kwargs)
def dbg(*args, **kwargs):          print_helper.dbg(prefix=print_prefix, *args, **kwargs)
def warn(*args, **kwargs):         print_helper.warn(prefix=print_prefix+' Warning:', *args, **kwargs)
def pink(*args, **kwargs):         print_helper.print_colored(prefix=print_prefix, color='magenta', *args, **kwargs)
def cyan(*args, **kwargs):         print_helper.print_colored(prefix=print_prefix, color='cyan', *args, **kwargs)
def red(*args, **kwargs):          print_helper.print_colored(prefix=print_prefix, color='red', *args, **kwargs)
def darkblue(*args, **kwargs):     print_helper.print_colored(prefix=print_prefix, color='darkblue', *args, **kwargs)
def darkgreen(*args, **kwargs):    print_helper.print_colored(prefix=print_prefix, color='darkgreen', *args, **kwargs)
def darkpink(*args, **kwargs):     print_helper.print_colored(prefix=print_prefix, color='darkpink', *args, **kwargs)
def lightyellow(*args, **kwargs):  print_helper.print_colored(prefix=print_prefix, color='lightyellow', *args, **kwargs)
def lightcyan(*args, **kwargs):    print_helper.print_colored(prefix=print_prefix, color='lightcyan', *args, **kwargs)
def lightred(*args, **kwargs):     print_helper.print_colored(prefix=print_prefix, color='lightred', *args, **kwargs)
def yellow(*args, **kwargs):       print_helper.print_colored(prefix=print_prefix, color='yellow', *args, **kwargs)
