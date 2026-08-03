"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'guyhopkins.com administration'

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('projects/', include("projects.urls"), name="project"),
    path('', include('web.urls'), name="web"),
]
