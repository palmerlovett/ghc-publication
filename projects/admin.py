from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Photo, ProjectPhoto, ArchitectDesigner, Owner
from django import forms
from django.conf import settings

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('photo_id', 'file')

@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(admin.ModelAdmin):
	list_display = ('photo', 'project',)

@admin.register(ArchitectDesigner)
class ArchitectDesigner(admin.ModelAdmin):
	list_display = ('name',)

@admin.register(Owner)
class Owner(admin.ModelAdmin):
	list_display = ('name',)