from django.contrib import admin

from models import Flag, Arrow
# Register your models here.

class FlagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ArrowAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Flag, FlagAdmin)
admin.site.register(Arrow, ArrowAdmin)