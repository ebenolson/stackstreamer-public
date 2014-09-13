from django import forms
from django.core.exceptions import ValidationError

from annotations.models import Flag


class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag

    def __init__(self, *args, **kwargs):

        #if kwargs.get('instance'):
        #    email = kwargs['instance'].email
        #    kwargs.setdefault('initial', {})['confirm_email'] = email

        return super(FlagForm, self).__init__(*args, **kwargs)