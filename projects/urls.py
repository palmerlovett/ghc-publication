from django.urls import path
#from django_distill import distill_path

from . import views

app_name = "projects"
urlpatterns = [
    path('', views.index, name="index"),
    #path('add/', views.add, name="add"),
    #path('edit/<path:project_slug>/', views.edit, name="edit"),
    path('<path:project_slug>/', views.project, name="project"),
    path('category/<path:category>', views.index, name="filter category"),
    path('engineer/<path:designer>', views.index, name="filter designer"),
    path('owner/<path:owner>', views.index, name="filter owner")
]
