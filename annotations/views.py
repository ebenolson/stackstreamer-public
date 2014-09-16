from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from stackstreamer.prettyprint import *

from django.views.generic.edit import FormView, CreateView

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.contrib.auth.decorators import login_required


from annotations.models import Flag
import forms

class CreateFlagView(CreateView):

    model = Flag
    form_class = forms.FlagForm

@login_required
def list_flags(request):
    flags = Flag.objects.all()
    # View code here...
    return render(request, 'list_flags.html', {"flags": flags, },
        content_type="text/html")    

@login_required
def delete_flag(request, id):
    try:
        flag = Flag.objects.get(id=id)
        flag.delete()
        return HttpResponse('')
    except ObjectDoesNotExist, MultipleObjectsReturned:
        dbg('flag with id %s not found'%id)
        return HttpResponseBadRequest('')