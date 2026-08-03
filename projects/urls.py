from django.urls import path
#from django_distill import distill_path

from . import views

app_name = "projects"
urlpatterns = [
    path('', views.index, name="index"),
    #path('add/', views.add, name="add"),
    #path('edit/<path:project_slug>/', views.edit, name="edit"),
    path('<path:project_slug>/', views.project, name="project"),
]
