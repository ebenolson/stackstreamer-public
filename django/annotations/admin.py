from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from models import Flag, Arrow
# Register your models here.

class FlagAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name',)

class ArrowAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Flag, FlagAdmin)
admin.site.register(Arrow, ArrowAdmin)