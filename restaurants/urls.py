from django.contrib import admin
from django.urls import path, include
from . import views
from .views import SalesChartData
# from .views import GeneratePdf

app_name = 'restaurants'

urlpatterns = [
    path('', views.home_view, name='home'),
    # path('pdf/', GeneratePdf.as_view()),
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
    path('addbillfoodmenu/', views.addbillfoodmenu_view, name='addbillfoodmenu'),
    path('editbillfoodmenu/', views.editbillfoodmenu_view, name='editbillfoodmenu'),
    path('cancelbillfoodmenu/', views.cancelbillfoodmenu_view, name='cancelbillfoodmenu'),
    path('sales/', views.sales_view, name='sales'),

    # Tables Section
    path('tablelist/', views.tablelist_view, name='tablelist'),
    path('addtable/', views.addtable_view, name='addtable'),
    path('edittable/', views.edittable_view, name='edittable'),
    path('deletetable/', views.deletetable_view, name='deletetable'),

    # Food Menu Section
    path('foodmenulist/', views.foodmenulist_view, name='foodmenulist'),
    path('addfoodmenulist/', views.addfoodmenulist_view, name='addfoodmenulist'),
    path('editfoodmenulist/', views.editfoodmenulist_view, name='editfoodmenulist'),
    path('deletefoodmenulist/', views.deletefoodmenulist_view, name='deletefoodmenulist'),

    # Food Category Section
    path('foodcategorylist/', views.foodcategorylist_view, name='foodcategorylist'),
    path('addfoodcategorylist/', views.addfoodcategorylist_view, name='addfoodcategorylist'),
    path('editfoodcategorylist/', views.editfoodcategorylist_view, name='editfoodcategorylist'),
    path('deletefoodcategorylist/', views.deletefoodcategorylist_view, name='deletefoodcategorylist'),

    # Close Transaction
    path('closetransaction/', views.closetransaction_view, name='closetransaction'),
    path('addcashremit/', views.addcashremit_view, name='addcashremit'),
    path('closed/', views.closed_view, name='closed'),

    # VOID 
    path('void/', views.void_view, name='void'),
    path('voidmenu/', views.voidmenu_view, name='voidmenu'),

    # TRANSACTION VOID
    path('transvoidfoodmenu/', views.transvoidfoodmenu_view, name='transvoidfoodmenu'),
    path('takeouttransvoidfoodmenu/', views.takeouttransvoidfoodmenu_view, name='takeouttransvoidfoodmenu'),

    # PAYMENT
    path('addamounttendered/', views.addamounttendered_view, name='addamounttendered'),

    # POS Settings
    path('possettings/', views.possettings_view, name='possettings'),
    path('editpossettings/', views.editpossettings_view, name='editpossettings'),

    # GENERATE RECEIPT
    path('pdf/', views.generatePdf, name='pdf'),
    path('bill/', views.generateBill, name='bill'),
    path('generatereceipt/', views.generateReceipt, name='generatereceipt'),
    path('generatebill/', views.generate_bill, name='generatebill'),
    path('downloaddine/<int:tableNo>/<int:refNo>/', views.downloaddine_view, name='downloaddine'),
    path('printdine/', views.printdine_view, name='printdine'),
    path('printtakeout/', views.printtakeout_view, name='printtakeout'),

    # REPORTS
    path('reports/', views.reports_view, name='reports'),
    path('api/saleschartdata/data/', SalesChartData.as_view()),

    # TRANSFER TABLE
    path('transfertable/', views.transfertable_view, name='transfertable'),

    
    path('sample/', views.sample_view, name='sample'),

]