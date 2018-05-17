from django.db import models

# Create your models here.
class FoodCategory(models.Model):
    categoryName        = models.CharField(max_length=255, blank=True, null=True)
    isVat               = models.BooleanField(default=False)    
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.categoryName

class Printer(models.Model):
    location            = models.CharField(max_length=255, blank=True, null=True)
    port                = models.CharField(max_length=10, blank=True, null=True) 
    isVat               = models.BooleanField(default=False) 
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.location

class FoodMenu(models.Model):
    foodCode            = models.CharField(max_length=255, blank=True, null=True)
    foodMenu            = models.CharField(max_length=255, blank=True, null=True)
    menuCategory        = models.CharField(max_length=255, blank=True, null=True)
    cost                = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price               = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    isVat               = models.BooleanField(default=False)  
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.foodMenu

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
    beginningCash       = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
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

class RestaurantTable(models.Model):
    tableNo             = models.CharField(max_length=255, blank=True, null=True)
    tableName           = models.CharField(max_length=255, blank=True, null=True)
    tableStatus         = models.CharField(max_length=255, blank=True, null=True)
    isVat               = models.BooleanField(default=False) 
    addedBy             = models.CharField(max_length=255, blank=True, null=True)
    updatedBy           = models.CharField(max_length=255, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.tableNo

class TempRestaurantOrderDetail(models.Model):
    referenceNo         = models.CharField(max_length=255, blank=True, null=True)
    productCode         = models.CharField(max_length=255, blank=True, null=True)
    categoryCode        = models.CharField(max_length=255, blank=True, null=True)
    branchCode          = models.CharField(max_length=255, blank=True, null=True)
    barcode             = models.CharField(max_length=255, blank=True, null=True)
    description         = models.CharField(max_length=255, blank=True, null=True)
    cost                = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sellingPrice        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    qtySold             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    prevQty             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    unitMeasure         = models.CharField(max_length=255, blank=True, null=True)
    taxRate             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    taxTotal            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    subTotal            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    income              = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    isHold              = models.BooleanField(default=False)
    isConfirmed         = models.BooleanField(default=False)
    isCancelled         = models.BooleanField(default=False)
    isVoid              = models.BooleanField(default=False)
    isErrorCorrect      = models.BooleanField(default=False)
    isVat               = models.BooleanField(default=True)
    holdBy              = models.CharField(max_length=255, blank=True, null=True)
    cancelledBy         = models.CharField(max_length=255, blank=True, null=True)
    voidBy              = models.CharField(max_length=255, blank=True, null=True)
    processedBy         = models.CharField(max_length=255, blank=True, null=True)
    totalAmount         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status              = models.CharField(max_length=255, blank=True, null=True)
    tableNo             = models.CharField(max_length=255, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.referenceNo

class TempRestaurantOrderSummary(models.Model):
    referenceNo         = models.CharField(max_length=255, blank=True, null=True)
    totalItem           = models.CharField(max_length=255, blank=True, null=True)
    totalSellingPrice   = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalTax            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalQty            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    subTotal            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalAmount         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalIncome         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalVATSale        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalVATExempSale   = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalVATableSale    = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    isFloat             = models.BooleanField(default=True)
    isVat               = models.BooleanField(default=True)
    preparedBy          = models.CharField(max_length=255, blank=True, null=True)
    status              = models.CharField(max_length=255, blank=True, null=True)
    tableNo             = models.CharField(max_length=255, blank=True, null=True)
    orderType           = models.CharField(max_length=255, blank=True, null=True)
    roomNumber          = models.CharField(max_length=255, blank=True, null=True)
    bookingNo           = models.CharField(max_length=255, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.referenceNo

class RestaurantOrderDetail(models.Model):
    orderNo             = models.CharField(max_length=255, blank=True, null=True)
    referenceNo         = models.CharField(max_length=255, blank=True, null=True)
    transactionCode     = models.CharField(max_length=255, blank=True, null=True)
    productCode         = models.CharField(max_length=255, blank=True, null=True)
    categoryCode        = models.CharField(max_length=255, blank=True, null=True)
    branchCode          = models.CharField(max_length=255, blank=True, null=True)
    barcode             = models.CharField(max_length=255, blank=True, null=True)
    description         = models.CharField(max_length=255, blank=True, null=True)
    cost                = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sellingPrice        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    qtySold             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    prevQty             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    unitMeasure         = models.CharField(max_length=255, blank=True, null=True)
    discountRate        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discountTotal       = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    chargeRate          = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    chargeTotal         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    taxRate             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    taxTotal            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    subTotal            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    income              = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    isHold              = models.BooleanField(default=False)
    isConfirmed         = models.BooleanField(default=False)
    isCancelled         = models.BooleanField(default=False)
    isVoid              = models.BooleanField(default=False)
    isErrorCorrect      = models.BooleanField(default=False)
    isVat               = models.BooleanField(default=True)
    holdBy              = models.CharField(max_length=255, blank=True, null=True)
    cancelledBy         = models.CharField(max_length=255, blank=True, null=True)
    voidBy              = models.CharField(max_length=255, blank=True, null=True)
    processedBy         = models.CharField(max_length=255, blank=True, null=True)
    totalAmount         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status              = models.CharField(max_length=255, blank=True, null=True)
    tableNo             = models.CharField(max_length=255, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.orderNo

class RestaurantOrderSummary(models.Model):
    orderNo             = models.CharField(max_length=255, blank=True, null=True)
    referenceNo         = models.CharField(max_length=255, blank=True, null=True)
    transactionCode     = models.CharField(max_length=255, blank=True, null=True)
    totalItem           = models.CharField(max_length=255, blank=True, null=True)
    totalItemSold       = models.CharField(max_length=255, blank=True, null=True)
    totalItemCancelled  = models.CharField(max_length=255, blank=True, null=True)
    totalDiscount       = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalCharge         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalUnitPrice      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalSellingPrice   = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalTax            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalQty            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    subTotal            = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalAmount         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalIncome         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalVATSale        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalVATExempSale   = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalVATableSale    = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    amountTendered      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    amountChange        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    paymentType         = models.CharField(max_length=255, blank=True, null=True)
    isHold              = models.BooleanField(default=False)
    isVoid              = models.BooleanField(default=False)
    isErrorCorrect      = models.BooleanField(default=False)
    isFloat             = models.BooleanField(default=True)
    isVat               = models.BooleanField(default=True)
    preparedBy          = models.CharField(max_length=255, blank=True, null=True)
    status              = models.CharField(max_length=255, blank=True, null=True)
    tableNo             = models.CharField(max_length=255, blank=True, null=True)
    orderType           = models.CharField(max_length=255, blank=True, null=True)
    discountType        = models.CharField(max_length=255, blank=True, null=True)
    seniorControlNo     = models.CharField(max_length=255, blank=True, null=True)
    seniorName          = models.CharField(max_length=255, blank=True, null=True)
    roomNumber          = models.CharField(max_length=255, blank=True, null=True)
    bookingNo           = models.CharField(max_length=255, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated        = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.orderNo
