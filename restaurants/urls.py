from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home_view, name='home'),
    # path('dine/', views.dine_view, name='dine'),
    path('takeout/', views.takeout_view, name='takeout'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('dine/',
        include([ 
                path('', views.dine_view, name='dine'), 
                path('maindishes/', views.main_view, name='main'),
                path('beverages/', views.beverage_view, name='beverage'),
                path('salads/', views.salad_view, name='salad'),
                path('appetizers/', views.appetizer_view, name='appetizer'),
                
                ]),), 
]