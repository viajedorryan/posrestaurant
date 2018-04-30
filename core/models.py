from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    description         = models.CharField(max_length=255)
    isVat               = models.BooleanField(default=False)    
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.description

class Printer(models.Model):
    location            = models.CharField(max_length=255)
    port                = models.CharField(max_length=10) 
    isVat               = models.BooleanField(default=False) 
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.location

class Product(models.Model):
    description         = models.CharField(max_length=255)
    sellingPrice        = models.DecimalField(max_digits=8, decimal_places=2)
    productCategoryID   = models.CharField(max_length=255)
    printerID           = models.CharField(max_length=255)
    isVat               = models.BooleanField(default=False)  
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.description
        