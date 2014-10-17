from django.db import models
import datetime

from sorl.thumbnail import ImageField

from django.core.files import File 

from stackorg.models import Stack
from exportroi.export import export_snapshot

from stackstreamer import settings

# Create your models here.

class Annotation(models.Model):
    name = models.CharField(max_length=256, default='Untitled')
    thumbnail = ImageField(upload_to='thumbnails', blank=True)
    stack = models.ForeignKey(Stack, default=1)
    date_created = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True)
    pixel_x = models.FloatField(default=0)
    pixel_y = models.FloatField(default=0)
    layer = models.IntegerField(default=0)
    zoom = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name    

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            fn = export_snapshot(self.stack.uuid, self.layer, self.zoom, 
                self.pixel_x/2.0**self.zoom-400, self.pixel_y/2.0**self.zoom-400, 
                self.pixel_x/2.0**self.zoom+400, self.pixel_y/2.0**self.zoom+400)
            self.thumbnail.save(fn, File(open(settings.MEDIA_ROOT+fn,'rb')))
        super(Annotation, self).save(*args, **kwargs)

class Flag(Annotation):
    pass

class Arrow(Annotation):
    def label(self, value):
        res = ''
        while value-1 >= 0:
            value = value-1
            res = chr(ord('A')+value%26) + res
            value = value // 26
        return res

    def save(self, *args, **kwargs):
        if self.name == 'Untitled':
            self.name = self.label(len(Arrow.objects.filter(stack=self.stack))+1)
        if not self.thumbnail:
            fn = export_snapshot(self.stack.uuid, self.layer, self.zoom, 
                self.pixel_x/2.0**self.zoom-100, self.pixel_y/2.0**self.zoom-100, 
                self.pixel_x/2.0**self.zoom+100, self.pixel_y/2.0**self.zoom+100)
            self.thumbnail.save(fn, File(open(settings.MEDIA_ROOT+fn,'rb')))
        super(Annotation, self).save(*args, **kwargs)