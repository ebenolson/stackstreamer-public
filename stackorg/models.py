from django.db import models

# Create your models here.
class Project(models.Model):
	name = models.CharField(max_length=256)
	def __unicode__(self):
	    return self.name	

class Stack(models.Model):
	name = models.CharField(max_length=256)
	UUID = models.CharField(max_length=128)
	thumbnail = models.ImageField(upload_to='/thumbnails')
	project = models.ForeignKey(Project)
	date_acquired = models.DateField()
	description = models.TextField()
