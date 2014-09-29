from django.contrib import admin

from models import DataExport
# Register your models here.

class DataExportAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(DataExport, DataExportAdmin)