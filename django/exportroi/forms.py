from django import forms
from django.core.exceptions import ValidationError

from exportroi.models import DataExport


class DataExportForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'stack', 'description', 'pixel_x0', 'pixel_x1', 'pixel_y0', 'pixel_y1', 'layer0', 'layer1']
        model = DataExport
    def __init__(self, *args, **kwargs):
        super(DataExportForm, self).__init__(*args, **kwargs)
        for field in ['stack', 'pixel_x0', 'pixel_x1', 'pixel_y0', 'pixel_y1', 'layer0', 'layer1']:
            self.fields[field].widget = forms.HiddenInput()
            #I know this can be done other ways too
