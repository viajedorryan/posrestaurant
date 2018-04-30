from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView

# app_name='web'
urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    # path('about', views.about, name='about'),
    # path('contact', views.contact, name='contact'),
    # path('properties', views.properties, name='properties'),
    # path('property/detail/<int:property_id>', views.property_detail, name='detail'),
    # path('search', views.search, name='search'),
]