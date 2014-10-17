from django.contrib import admin

from models import Project, Stack
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name',)
	fields = ('name',)

class StackAdmin(admin.ModelAdmin):
	readonly_fields = ('thumb_tag',)
	exclude = ('thumbnail',)
	
admin.site.register(Project, ProjectAdmin)
admin.site.register(Stack, StackAdmin)