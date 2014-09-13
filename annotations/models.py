from django.db import models
import datetime

from stackorg.models import Stack
# Create your models here.

class Annotation(models.Model):
    name = models.CharField(max_length=256, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)
    stack = models.ForeignKey(Stack, default=1)
    date_created = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True)
    pixel_x = models.FloatField(default=0)
    pixel_y = models.FloatField(default=0)
    layer = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name    
    def thumb_tag(self):
        return u'<img src="%s" />' % self.thumbnail.url
    thumb_tag.short_description = 'Thumbnail'
    thumb_tag.allow_tags = True

class Flag(Annotation):
    pass

class Arrow(Annotation):
    rotation = models.FloatField(default=0)