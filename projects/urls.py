from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('<path:project_slug>', views.project, name="project"),
    path('admin', views.add, name="add"),
    path('admin/<path:project_slug>', views.edit, name="edit")
]
