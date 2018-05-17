from django.contrib import admin
from .models import *

# Register your models here.
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoryName', 'isVat', 'date_created', 'date_updated')

class PrinterAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'port', 'isVat', 'date_created', 'date_updated')

class FoodMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'foodCode', 'foodMenu', 'menuCategory', 'cost', 'price', 'isVat', 'date_created', 'date_updated')

class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'branchCode', 'branchName', 'branchAddress', 'isVat', 'date_created', 'date_updated')

class POSSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'branchCode', 'posName', 'companyName', 'address1', 'address2', 'tinNo', 'minNo', 'birPermitNo', 'serialNo', 'isVat', 'date_created', 'date_updated')

class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'tableNo', 'tableName', 'tableStatus', 'addedBy', 'updatedBy', 'isVat', 'date_created', 'date_updated')

class TempRestaurantOrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'referenceNo', 'isVat', 'date_created', 'date_updated')

class TempRestaurantOrderSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'referenceNo', 'isVat', 'date_created', 'date_updated')

class RestaurantOrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderNo', 'referenceNo', 'transactionCode', 'isVat', 'date_created', 'date_updated')

class RestaurantOrderSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderNo', 'referenceNo', 'transactionCode', 'isVat', 'date_created', 'date_updated')

admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(Printer, PrinterAdmin)
admin.site.register(FoodMenu, FoodMenuAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(POSSetting, POSSettingAdmin)
admin.site.register(SalesTransactionSummary)
admin.site.register(RestaurantTable, RestaurantTableAdmin)
admin.site.register(TempRestaurantOrderDetail, TempRestaurantOrderDetailAdmin)
admin.site.register(TempRestaurantOrderSummary, TempRestaurantOrderSummaryAdmin)
admin.site.register(RestaurantOrderDetail, RestaurantOrderDetailAdmin)
admin.site.register(RestaurantOrderSummary, RestaurantOrderSummaryAdmin)