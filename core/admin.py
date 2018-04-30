from django.contrib import admin
from .models import *

# Register your models here.
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'description', 'isVat', 'date_created', 'date_updated')

admin.site.register(ProductCategory)
admin.site.register(Printer)
admin.site.register(Product)