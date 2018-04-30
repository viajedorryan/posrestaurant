from django.contrib import admin
from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dine/', views.dine_view, name='dine'),
    path('takeout/', views.takeout_view, name='takeout'),
    path('delivery/', views.delivery_view, name='delivery'),
]