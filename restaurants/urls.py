from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home_view, name='home'),
    # path('dine/', views.dine_view, name='dine'),
    path('takeout/', views.takeout_view, name='takeout'),
    path('cashin/', views.cashin_view, name='cashin'),
    path('dine/', views.dines_view, name='dines'),
    path('dine/<int:tableNo>/', views.dine_view, name='dine'),
    path('addfoodmenu/', views.addfoodmenu_view, name='addfoodmenu'),
    path('editfoodmenu/', views.editfoodmenu_view, name='editfoodmenu'),
    path('savefoodmenu/', views.savefoodmenu_view, name='savefoodmenu'),
    path('cancelfoodmenu/', views.cancelfoodmenu_view, name='cancelfoodmenu'),
    path('takeoutfoodmenu/', views.takeoutfoodmenu_view, name='takeoutfoodmenu'),
    path('edittakeoutfoodmenu/', views.edittakeoutfoodmenu_view, name='edittakeoutfoodmenu'),
    path('canceltakeoutfoodmenu/', views.canceltakeoutfoodmenu_view, name='canceltakeoutfoodmenu'),
    path('paytakeoutfoodmenu/', views.paytakeoutfoodmenu_view, name='paytakeoutfoodmenu'),
    path('billing/<int:tableNo>/', views.billing_view, name='billing'),
    path('payment/', views.payment_view, name='payment'),
]