from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    description         = models.CharField(max_length=255, blank=True, null=True)
    isVat               = models.BooleanField(default=False)    
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.description

class Printer(models.Model):
    location            = models.CharField(max_length=255, blank=True, null=True)
    port                = models.CharField(max_length=10, blank=True, null=True) 
    isVat               = models.BooleanField(default=False) 
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.location

class Product(models.Model):
    branchCode          = models.CharField(max_length=255, blank=True, null=True)
    productCode         = models.CharField(max_length=255, blank=True, null=True)
    description         = models.CharField(max_length=255, blank=True, null=True)
    sellingPrice        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    productCategoryID   = models.CharField(max_length=255, blank=True, null=True)
    printerID           = models.CharField(max_length=255, blank=True, null=True)
    isVat               = models.BooleanField(default=False)  
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.description

class Branch(models.Model):
    branchCode          = models.CharField(max_length=255, blank=True, null=True)
    branchName          = models.CharField(max_length=255, blank=True, null=True)
    branchAddress       = models.CharField(max_length=255, blank=True, null=True)
    isVat               = models.BooleanField(default=False)    
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.branchName

class POSSetting(models.Model):
    branchCode          = models.CharField(max_length=255, blank=True, null=True)
    posName             = models.CharField(max_length=255, blank=True, null=True)
    companyName         = models.CharField(max_length=255, blank=True, null=True)
    address1            = models.CharField(max_length=255, blank=True, null=True)
    address2            = models.CharField(max_length=255, blank=True, null=True)
    tinNo               = models.CharField(max_length=255, blank=True, null=True)
    minNo               = models.CharField(max_length=255, blank=True, null=True)
    birPermitNo         = models.CharField(max_length=255, blank=True, null=True)
    serialNo            = models.CharField(max_length=255, blank=True, null=True)
    isVat               = models.BooleanField(default=False) 
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.companyName

class SalesTransactionSummary(models.Model):
    accountCode         = models.CharField(max_length=255, blank=True, null=True)
    branchCode          = models.CharField(max_length=255, blank=True, null=True)
    userID              = models.CharField(max_length=255, blank=True, null=True)
    beginningCash       = models.DecimalField(max_digits=8, decimal_places=2)
    beginningInvoice    = models.CharField(max_length=255, blank=True, null=True)
    beginningOR         = models.CharField(max_length=255, blank=True, null=True)
    lastOR              = models.CharField(max_length=255, blank=True, null=True)
    lastTransactionNo   = models.CharField(max_length=255, blank=True, null=True)
    nextBeginningCash   = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    noOfSoldItem        = models.IntegerField(blank=True, null=True)
    totalSoldItem       = models.IntegerField(blank=True, null=True)
    noOfCancelledItem   = models.IntegerField(blank=True, null=True)
    totalCancelledItem  = models.IntegerField(blank=True, null=True)
    totalSales          = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalCashSales      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalCash           = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cashRemitted        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    openBy              = models.CharField(max_length=255, blank=True, null=True)
    closedBy            = models.CharField(max_length=255, blank=True, null=True)
    shortage            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    isVat               = models.BooleanField(default=False) 
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.accountCode