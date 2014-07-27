from django.contrib import admin

from models import Project, Stack
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name',)
	fields = ('name',)

class StackAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Project, ProjectAdmin)
admin.site.register(Stack, StackAdmin)