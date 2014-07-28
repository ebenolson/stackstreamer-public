from django.db import models
import datetime

# Create your models here.
class Project(models.Model):
	name = models.CharField(max_length=256)
	def __unicode__(self):
	    return self.name	

class Stack(models.Model):
	name = models.CharField(max_length=256)
	uuid = models.CharField(max_length=128)
	thumbnail = models.ImageField(upload_to='thumbnails')
	project = models.ForeignKey(Project, default=1)
	date_acquired = models.DateField(default=datetime.date.today)
	description = models.TextField(blank=True)
	pixel_size = models.FloatField(default=0)
	pixel_width = models.IntegerField(default=0)
	pixel_height = models.IntegerField(default=0)
	slice_spacing = models.FloatField(default=0)
	n_slices = models.IntegerField(default=0)
	def __unicode__(self):
	    return self.name	
	def thumb_tag(self):
	    return u'<img src="%s" />' % self.thumbnail.url
	thumb_tag.short_description = 'Thumbnail'
	thumb_tag.allow_tags = True