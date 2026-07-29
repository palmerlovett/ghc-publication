from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact-us/', views.contact, name='contact')
]
