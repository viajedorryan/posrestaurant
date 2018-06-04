from django.contrib import admin
from django.urls import path, include
from . import views
# from .views import GeneratePdf

app_name = 'orderstations'

urlpatterns = [
    path('', views.orderstation_view, name='orderstation'),

    # DINE
    path('dine/', views.orderdine_view, name='orderdine'),
    path('dine/<int:tableNo>/<int:waiterID>/', views.viewdine_view, name='viewdine'),
    path('adddineorder/', views.adddineorder_view, name='adddineorder'),
    path('savedineorder/', views.savedineorder_view, name='savedineorder'),
    path('canceldineorder/', views.canceldineorder_view, name='canceldineorder'),

    # TAKEOUT
    path('takeout/<int:waiterID>/', views.ordertakeout_view, name='ordertakeout'),
    path('addordertakeout/', views.addordertakeout_view, name='addordertakeout'),

    path('checkwaiter/', views.checkwaiter_view, name='checkwaiter'),
    path('checkwaitertakeout/', views.checkwaitertakeout_view, name='checkwaitertakeout'),
    path('printorders/<int:tableNo>/<int:waiterID>/', views.printorders_view, name='printorders'),

]