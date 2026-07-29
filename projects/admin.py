from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Photo, Project, ArchitectDesigner
from django import forms
from django.conf import settings

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title','completion_date', 'project_value')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('project', 'name')

@admin.register(ArchitectDesigner)
class ArchitectDesigner(admin.ModelAdmin):
	list_display = ('name')