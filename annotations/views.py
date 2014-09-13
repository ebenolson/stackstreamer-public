from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView

from annotations.models import Flag
import forms

class CreateFlagView(CreateView):

    model = Flag
    form_class = forms.FlagForm