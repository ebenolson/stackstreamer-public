from django.db import models
import datetime

from sorl.thumbnail import ImageField

from django.core.files import File 

from stackorg.models import Stack
from exportroi.export import export_snapshot

from stackstreamer import settings

# Create your models here.

class DataExport(models.Model):
    name = models.CharField(max_length=256, default='Untitled')
    thumbnail = ImageField(upload_to='thumbnails', blank=True)
    stack = models.ForeignKey(Stack, default=1)
    date_created = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True)
    pixel_x0 = models.FloatField(default=0)
    pixel_y0 = models.FloatField(default=0)
    pixel_x1 = models.FloatField(default=0)
    pixel_y1 = models.FloatField(default=0)
    layer0 = models.IntegerField(default=0)
    layer1 = models.IntegerField(default=0)
    zoom = models.IntegerField(default=0)
    completion = models.FloatField(default=0)
    filename = models.FileField(upload_to='export', blank=True)

    def layers(self):
        return self.layer1-self.layer0+1

    def get_absolute_url():
        return '/'
        
    def __unicode__(self):
        return self.name
