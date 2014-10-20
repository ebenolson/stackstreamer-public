from __future__ import absolute_import

from celery import shared_task

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files import File 
from django.db.models.signals import post_save
from django.dispatch import receiver

import os, uuid

from stackstreamer.prettyprint import *
from stackstreamer import settings

from exportroi.models import DataExport
from exportroi.export import export_snapshot

@shared_task
def prepare_data_export(id):
    try:
        de = DataExport.objects.get(pk=id)
    except ObjectDoesNotExist, MultipleObjectsReturned:
        dbg('DataExport not found')
        return False

    if de.layer0 == de.layer1:
        fn = export_snapshot(de.stack.uuid, de.layer0, de.zoom, de.pixel_x0, de.pixel_y0, de.pixel_x1, de.pixel_y1)
        de.filename = fn
        de.completion = 100
        de.save()
        de.thumbnail.save(fn, File(open(settings.MEDIA_ROOT+fn,'rb')))
        return True
    else:
        dirname = 'export/%s'%uuid.uuid4()
        try:
            os.makedirs(settings.MEDIA_ROOT+dirname)
        except OSError:
            pass

        for l in range(de.layer0, de.layer1):
            fn = export_snapshot(de.stack.uuid, l, de.zoom, de.pixel_x0, de.pixel_y0, de.pixel_x1, de.pixel_y1)
            if l == de.layer0:
                de.thumbnail.save(fn, File(open(settings.MEDIA_ROOT+fn,'rb')))
                de.save()
            os.rename(settings.MEDIA_ROOT+fn, '%s/layer_%04d.png'%(settings.MEDIA_ROOT+dirname,l))

        os.system('zip -0 -j -r -m %s.zip %s'%(settings.MEDIA_ROOT+dirname, settings.MEDIA_ROOT+dirname))
        os.rmdir(settings.MEDIA_ROOT+dirname)
        de.filename = dirname+'.zip'
        de.completion = 100
        de.save()
        return True

    return False

@receiver(post_save, sender=DataExport)
def check_for_preparation(sender, instance, **kwargs):
    dbg("checking")
    if instance.completion == 0:
        instance.completion = 1
        prepare_data_export.delay(instance.pk)
