from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from stackstreamer.prettyprint import *

from django.views.generic.edit import FormView, CreateView

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.contrib.auth.decorators import login_required


from annotations.models import Flag, Arrow
import forms

class CreateFlagView(CreateView):
    model = Flag
    form_class = forms.FlagForm

@login_required
def list_flags(request, stack):
    flags = Flag.objects.filter(stack=stack)
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

@login_required
def edit_flag_text(request):
    id = request.POST['pk']
    value = request.POST['value']
    try:
        flag = Flag.objects.get(id=id)
        flag.name = value
        flag.save()
        return HttpResponse('')
    except ObjectDoesNotExist, MultipleObjectsReturned:
        dbg('flag with id %s not found'%id)
        return HttpResponseBadRequest('')


class CreateArrowView(CreateView):
    model = Arrow
    form_class = forms.ArrowForm

@login_required
def list_arrows(request, stack):
    arrows = Arrow.objects.filter(stack=stack)
    # View code here...
    return render(request, 'list_arrows.html', {"arrows": arrows, },
        content_type="text/html")    

@login_required
def marker_list(request, stack):
    arrows = Arrow.objects.filter(stack=stack)
    # View code here...
    return render(request, 'marker_list.html', {"arrows": arrows, },
        content_type="text/html")    

@login_required
def delete_arrow(request, id):
    try:
        arrow = Arrow.objects.get(id=id)
        arrow.delete()
        return HttpResponse('')
    except ObjectDoesNotExist, MultipleObjectsReturned:
        dbg('arrow with id %s not found'%id)
        return HttpResponseBadRequest('')

@login_required
def edit_arrow_text(request):
    id = request.POST['pk']
    value = request.POST['value']
    try:
        arrow = Arrow.objects.get(id=id)
        arrow.name = value
        arrow.save()
        return HttpResponse('')
    except ObjectDoesNotExist, MultipleObjectsReturned:
        dbg('arrow with id %s not found'%id)
        return HttpResponseBadRequest('')        