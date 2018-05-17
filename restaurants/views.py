from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from core.models import *
import datetime
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.
# function based view
def home_view(request):
    branches = Branch.objects.filter(isVat=True)
    users = request.user.id
    print(users)
    try:
        checks = SalesTransactionSummary.objects.get(userID=users, isVat=1)
    except SalesTransactionSummary.DoesNotExist:
        checks = None

    template='home.html'
    context = {'branches': branches, 'checks': checks, 'time':datetime.date.today()}
    return render(request, template, context)


def cashin_view(request):
    if request.method == 'POST':
        code = request.POST.get('branchcode')
        name = request.POST.get('branchname')
        cashbegin = request.POST.get('cashbegin')
        user = request.user.id
        salessummary = SalesTransactionSummary.objects.filter(isVat=True).count()

        if salessummary != None:
            accntcode = salessummary + 1000
            sales = SalesTransactionSummary(
                accountCode=accntcode,
                branchCode=code,
                userID=user,
                beginningCash=cashbegin,
                openBy=user,
                isVat=True
                )
            
            sales.save()

    template='home.html'
    context = {}
    return render(request, template, context)


def takeout_view(request):
    # Fetch all FoodMenu
    menus = FoodMenu.objects.all()

    #Fetch all RestaurantOrderSummary that isVal=True
    countOrderSummaries = RestaurantOrderSummary.objects.all().count()
    totalOrderSummaries = countOrderSummaries + 1000

    getSalesTransactionSummary = SalesTransactionSummary.objects.get(userID=request.user.id, isVat=True)
    print(getSalesTransactionSummary)

    getOrderDetailsLists = RestaurantOrderDetail.objects.filter(orderNo=totalOrderSummaries)
    
    try:
        totalamount = RestaurantOrderDetail.objects.filter(isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
    except RestaurantOrderDetail.DoesNotExist:
        totalamount = None
        raise Http404("No MyModel matches the given query.")

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12
    
    try:
        totalitems = RestaurantOrderDetail.objects.filter(isVat=True).aggregate(sum=Sum('qtySold'))['sum']
    except RestaurantOrderDetail.DoesNotExist:
        totalitems = None
        raise Http404("No MyModel matches the given query.")

    tempOrderDetails = RestaurantOrderDetail.objects.filter(orderNo=totalOrderSummaries, isVat=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(tempOrderDetails, 10)
    try:
        tempOrderDetailpages = paginator.page(page)
    except PageNotAnInteger:
        tempOrderDetailpages = paginator.page(1)
    except EmptyPage:
        tempOrderDetailpages = paginator.page(paginator.num_pages)
        
    template='takeout.html'
    context = {'tempOrderDetailpages': tempOrderDetailpages,'menus': menus, 'totalOrderSummaries': totalOrderSummaries,'getSalesTransactionSummary': getSalesTransactionSummary,'getOrderDetailsLists': getOrderDetailsLists,'totalamount': totalamount,'totalitems': totalitems,'totalVATsale': totalVATsale,'totalVAT': totalVAT}
    return render(request, template, context)

def takeoutfoodmenu_view(request):
    if request.method == 'POST':
        orderno         = request.POST.get("orderNo") 
        transid         = request.POST.get("transID")  
        prodcode        = request.POST.get("prodCode") 
        foodDesc        = request.POST.get("foodDesc")  
        foodSellPrice   = request.POST.get("foodSellPrice")  

        # getqty = float(foodSellPrice) *
        taxrate = 0.12
        subtotal = float(foodSellPrice) / 1.12
        totaltax = subtotal * taxrate

        saveRestaurantOrderDetail = RestaurantOrderDetail(
                    orderNo=orderno,
                    transactionCode=transid,
                    productCode=prodcode,
                    branchCode=888,
                    description=foodDesc,
                    sellingPrice=foodSellPrice,
                    qtySold=1,
                    taxRate=taxrate,
                    taxTotal=totaltax,
                    subTotal=subtotal,
                    processedBy=request.user.username,
                    totalAmount=foodSellPrice,
                    status='Pending'
                )
        saveRestaurantOrderDetail.save()
    return redirect('restaurants:takeout')

def edittakeoutfoodmenu_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("id") 
        orderno        = request.POST.get("ref") 
        qty         = request.POST.get("qty") 

        try:
            getexists = RestaurantOrderDetail.objects.filter(orderNo=orderno, id=idno, isVat=True, isCancelled=False)
        except TempRestaurantOrderDetail.DoesNotExist:
            getexists = None
            raise Http404("No MyModel matches the given query.")

        if getexists is not None:
            for getexist in getexists:
                taxrate = 0.12
                gettotal = float(getexist.sellingPrice) * float(qty)
                updatesubtotal = float(gettotal) / 1.12
                updatetotaltax = updatesubtotal * taxrate

                RestaurantOrderDetail.objects.filter(orderNo=orderno, id=idno, isVat=True, isCancelled=False).update(qtySold=qty, totalAmount=gettotal, taxTotal=updatetotaltax, subTotal=updatesubtotal)
        return redirect('restaurants:takeout')
    return redirect('restaurants:takeout')

def canceltakeoutfoodmenu_view(request):
    if request.method == 'POST':
        idno         = request.POST.get("idno") 
        print(idno)
        RestaurantOrderDetail.objects.filter(id=idno, isVat=True).update(isCancelled=True, isVat=False, status='Cancelled')

    return redirect('restaurants:takeout')

def paytakeoutfoodmenu_view(request):
    if request.method == 'POST':
        orderno         = request.POST.get("orderNo") 
        transid         = request.POST.get("transID")  
        amounttender    = request.POST.get("amounttender")
        amountpayable   = request.POST.get("amountpayable")
        print(orderno)
        print(transid)
        print(amounttender)
        print(amountpayable)
        
        if float(amountpayable) > float(amounttender) or float(amountpayable) == 0:
            messages.warning(request, 'Tender Amount must not less than Amount Payable or Amount Payable must not equal to zero')
            return redirect('restaurants:takeout')
        else:
            getOrderSummaryinfos =  RestaurantOrderSummary.objects.filter(orderNo=orderno, transactionCode=transid, isVat=True)

            if getOrderSummaryinfos.exists():
                return redirect('restaurants:takeout')
            else:
                amountChange = float(amounttender) - float(amountpayable)
                print(amountChange)
                
                # For orderNo
                print(orderno)

                # For transactionCode
                print(transid)

                # For totalItem
                gettotalItem = RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
                print(gettotalItem)

                # For totalSellingPrice
                gettotalSellingPrice = RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
                print(gettotalSellingPrice)

                # For totalTax
                if not gettotalSellingPrice:
                    gettotalSellingPrice = 0
                totalVATsale = float(gettotalSellingPrice) / 1.12
                totalVAT = totalVATsale * 0.12
                print(totalVAT)

                # For totalQty
                gettotalQty = RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
                print(gettotalQty)

                # For totalSubTotal
                gettotalSubTotal = float(gettotalSellingPrice) - float(totalVAT)
                print(gettotalSubTotal)

                # For totalAmount
                print(gettotalSellingPrice)

                # For totalVATSale
                print(totalVATsale)

                # For status
                print('SOLD')

                # For orderType
                print('TAKEOUT')

                
                saveOrderSummary = RestaurantOrderSummary(
                            orderNo=orderno,
                            transactionCode=transid,
                            totalItem=gettotalItem,
                            totalItemSold=gettotalItem,
                            totalSellingPrice=gettotalSellingPrice,
                            totalUnitPrice=gettotalSellingPrice,
                            totalTax=totalVAT,
                            totalQty=gettotalQty,
                            subTotal=gettotalSubTotal,
                            totalAmount=gettotalSellingPrice,
                            totalVATSale=totalVATsale,
                            preparedBy=request.user.username,
                            status='SOLD',
                            orderType='TAKEOUT',
                            paymentType='CASH',
                            isVat=False,
                            amountTendered=amounttender,
                            amountChange=amountChange
                        )
                saveOrderSummary.save()

                RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=True).update(isVat=False, status='SOLD')
    
    messages.success(request, 'Payment Success')
    return redirect('restaurants:takeout')
    
def dines_view(request):
    tables = RestaurantTable.objects.all()
    template='tables.html'
    context = {'tables': tables}
    return render(request, template, context)

def payment_view(request):

    if request.method == 'POST':
        tableno         = request.POST.get("tableNo") 
        transcode       = request.POST.get("transCode") 
        orderno         = request.POST.get("orderNo") 
        amounttender    = request.POST.get("amounttender")
        amountpayable   = request.POST.get("amountpayable")
        print(tableno)
        print(transcode)
        print(orderno)
        print(float(amounttender))
        print(amountpayable)
        if float(amountpayable) > float(amounttender):
            messages.warning(request, 'Tender Amount must not less than Amount Payable')
            return HttpResponseRedirect('/restaurants/billing/'+tableno)
        else:
            amountChange = float(amounttender) - float(amountpayable)
            print(amountChange)
            tempOrderDetails = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True, isCancelled=False)
            print(tempOrderDetails)
            for tempOrderDetail in tempOrderDetails:
                print(tempOrderDetail)
                saveOrderDetail = RestaurantOrderDetail(
                            orderNo=orderno,
                            referenceNo=tempOrderDetail.referenceNo,
                            transactionCode=transcode,
                            productCode=tempOrderDetail.productCode,
                            description=tempOrderDetail.description,
                            sellingPrice=tempOrderDetail.sellingPrice,
                            qtySold=tempOrderDetail.qtySold,
                            taxRate=tempOrderDetail.taxRate,
                            taxTotal=tempOrderDetail.taxTotal,
                            subTotal=tempOrderDetail.subTotal,
                            processedBy=request.user.username,
                            totalAmount=tempOrderDetail.totalAmount,
                            status='SOLD',
                            isVat=False,
                            tableNo=tempOrderDetail.tableNo
                        )
                saveOrderDetail.save()
                TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True, isCancelled=False).update(isVat=False, status='SOLD')
            getOrderSummaryinfos = TempRestaurantOrderSummary.objects.get(tableNo=tableno, isVat=True)
            print(getOrderSummaryinfos)

            # for getOrderSummaryinfo in getOrderSummaryinfos:
            #     print(getOrderSummaryinfo)
            saveOrderSummary = RestaurantOrderSummary(
                        orderNo=orderno,
                        referenceNo=getOrderSummaryinfos.referenceNo,
                        transactionCode=transcode,
                        totalItem=getOrderSummaryinfos.totalItem,
                        totalItemSold=getOrderSummaryinfos.totalItem,
                        totalSellingPrice=getOrderSummaryinfos.totalSellingPrice,
                        totalUnitPrice=getOrderSummaryinfos.totalSellingPrice,
                        totalTax=getOrderSummaryinfos.totalTax,
                        totalQty=getOrderSummaryinfos.totalItem,
                        subTotal=getOrderSummaryinfos.subTotal,
                        totalAmount=getOrderSummaryinfos.totalAmount,
                        totalVATSale=getOrderSummaryinfos.totalVATSale,
                        preparedBy=request.user.username,
                        status='SOLD',
                        tableNo=getOrderSummaryinfos.tableNo,
                        orderType=getOrderSummaryinfos.orderType,
                        paymentType='CASH',
                        isVat=False,
                        amountTendered=amounttender,
                        amountChange=amountChange
                    )
            saveOrderSummary.save()
            TempRestaurantOrderSummary.objects.filter(tableNo=tableno, isVat=True).update(isVat=False, status='SOLD')

            RestaurantTable.objects.filter(tableNo=tableno, isVat=True).update(isVat=False, tableStatus='Available')
    return redirect('restaurants:dines')


def billing_view(request, tableNo):
    tables = RestaurantTable.objects.get(tableNo=tableNo)
    print(tables)

    #Fetch all RestaurantOrderSummary that isVal=True
    countOrderSummaries = RestaurantOrderSummary.objects.count()
    print(countOrderSummaries)
    totalOrderSummaries = countOrderSummaries + 1000
    print(totalOrderSummaries)

    getSalesTransactionSummary = SalesTransactionSummary.objects.get(userID=request.user.id, isVat=True)
    print(getSalesTransactionSummary)

    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(tableNo=tables, isVat=True, isCancelled=False)

    print(getOrderDetailsLists)
    for getOrderDetailsList in getOrderDetailsLists:

        tempOrderDetails = TempRestaurantOrderDetail.objects.filter(referenceNo=getOrderDetailsList.referenceNo, tableNo=tables, isVat=True)
        print(tempOrderDetails)
        page = request.GET.get('page', 1)

        paginator = Paginator(tempOrderDetails, 10)
        try:
            tempOrderDetailpages = paginator.page(page)
        except PageNotAnInteger:
            tempOrderDetailpages = paginator.page(1)
        except EmptyPage:
            tempOrderDetailpages = paginator.page(paginator.num_pages)
    
    try:
        totalamount = TempRestaurantOrderDetail.objects.filter(tableNo=tables, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
    except TempRestaurantOrderDetail.DoesNotExist:
        totalamount = None
        raise Http404("No MyModel matches the given query.")

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12
    
    try:
        totalitems = TempRestaurantOrderDetail.objects.filter(tableNo=tables, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
    except TempRestaurantOrderDetail.DoesNotExist:
        totalitems = None
        raise Http404("No MyModel matches the given query.")
        

    template='billing.html'
    context = {'tables': tables,'totalOrderSummaries': totalOrderSummaries,'getSalesTransactionSummary': getSalesTransactionSummary,'tempOrderDetailpages':tempOrderDetailpages,'totalamount': totalamount,'totalitems': totalitems,'totalVATsale': totalVATsale,'totalVAT': totalVAT}
    return render(request, template, context)


def dine_view(request, tableNo):
    tables = RestaurantTable.objects.get(tableNo=tableNo)
    print(tables)

    # Fetch all FoodMenu
    menus = FoodMenu.objects.all()

    #Fetch all RestaurantOrderSummary that isVal=True
    countOrderSummaries = RestaurantOrderSummary.objects.count()
    print(countOrderSummaries)
    totalOrderSummaries = countOrderSummaries + 1000
    print(totalOrderSummaries)

    #Fetch all TempRestaurantOrderSummary that isVal=True
    countTempOrderSummaries = TempRestaurantOrderSummary.objects.count()
    totalTempOrderSummaries = countTempOrderSummaries + 1000

    getSalesTransactionSummary = SalesTransactionSummary.objects.get(userID=request.user.id, isVat=True)
    print(getSalesTransactionSummary)

    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(referenceNo=totalTempOrderSummaries, tableNo=tables, isVat=True)
    
    try:
        totalamount = TempRestaurantOrderDetail.objects.filter(tableNo=tables, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
    except TempRestaurantOrderDetail.DoesNotExist:
        totalamount = None
        raise Http404("No MyModel matches the given query.")

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12
    
    try:
        totalitems = TempRestaurantOrderDetail.objects.filter(tableNo=tables, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
    except TempRestaurantOrderDetail.DoesNotExist:
        totalitems = None
        raise Http404("No MyModel matches the given query.")

    tempOrderDetails = TempRestaurantOrderDetail.objects.filter(referenceNo=totalTempOrderSummaries, tableNo=tables, isVat=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(tempOrderDetails, 10)
    try:
        tempOrderDetailpages = paginator.page(page)
    except PageNotAnInteger:
        tempOrderDetailpages = paginator.page(1)
    except EmptyPage:
        tempOrderDetailpages = paginator.page(paginator.num_pages)
        

    template='table.html'
    context = {'tables': tables,'tempOrderDetailpages': tempOrderDetailpages,'menus': menus,'totalTempOrderSummaries': totalTempOrderSummaries,'totalOrderSummaries': totalOrderSummaries,'getSalesTransactionSummary': getSalesTransactionSummary,'getOrderDetailsLists': getOrderDetailsLists,'totalamount': totalamount,'totalitems': totalitems,'totalVATsale': totalVATsale,'totalVAT': totalVAT}
    return render(request, template, context)
    
def addfoodmenu_view(request):
    if request.method == 'POST':
        refNo           = request.POST.get("refNo") 
        prodcode        = request.POST.get("prodCode") 
        foodDesc        = request.POST.get("foodDesc")  
        foodSellPrice   = request.POST.get("foodSellPrice")  
        tableno         = request.POST.get("tableNo")  

        # getqty = float(foodSellPrice) *
        taxrate = 0.12
        subtotal = float(foodSellPrice) / 1.12
        totaltax = subtotal * taxrate

        # try:
        #     getexists = TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, productCode=prodcode, tableNo=tableno, isVat=True, isCancelled=False)
        # except TempRestaurantOrderDetail.DoesNotExist:
        #     getexists = None
        #     raise Http404("No MyModel matches the given query.")
        # print(getexists)
        # if getexists is None:

        saveTempRestaurantOrderDetail = TempRestaurantOrderDetail(
                    referenceNo=refNo,
                    productCode=prodcode,
                    branchCode=888,
                    description=foodDesc,
                    sellingPrice=foodSellPrice,
                    qtySold=1,
                    unitMeasure='kg',
                    taxRate=taxrate,
                    taxTotal=totaltax,
                    subTotal=subtotal,
                    processedBy=request.user.username,
                    totalAmount=foodSellPrice,
                    status='Pending',
                    tableNo=tableno
                )
        saveTempRestaurantOrderDetail.save()
        # return HttpResponseRedirect('/restaurants/table/'+tableno)
        # if getexists is not None:
        #     for getexist in getexists:
        #         plusqty = float(getexist.qtySold) + 1
        #         gettotal = float(foodSellPrice) * plusqty
        #         updatesubtotal = float(gettotal) / 1.12
        #         updatetotaltax = updatesubtotal * taxrate

        #         TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, productCode=prodcode, tableNo=tableno, isVat=True).update(qtySold=plusqty, totalAmount=gettotal, taxTotal=updatetotaltax, subTotal=updatesubtotal)
        #         return HttpResponseRedirect('/restaurants/table/'+tableno)
    return HttpResponseRedirect('/restaurants/dine/'+tableno)

def savefoodmenu_view(request):
    if request.method == 'POST':
        refno           = request.POST.get("refNo")  
        tableno         = request.POST.get("tableNo")  
        print(refno)
        print(tableno)
        # getOrderDetailsinfos = TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True)[:1].get()
        # print(getOrderDetailsinfos.referenceNo)

        getOrderSummaryinfos =  TempRestaurantOrderSummary.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True)

        if getOrderSummaryinfos.exists():
            return HttpResponseRedirect('/restaurants/dine/'+tableno)
        else:
            # For totalItem
            gettotalItem = TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
            print(gettotalItem)

            # For totalSellingPrice
            gettotalSellingPrice = TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
            print(gettotalSellingPrice)

            # For totalTax
            if not gettotalSellingPrice:
                gettotalSellingPrice = 0
            totalVATsale = float(gettotalSellingPrice) / 1.12
            totalVAT = totalVATsale * 0.12
            print(totalVAT)

            # For totalQty
            gettotalQty = TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
            print(gettotalQty)

            # For totalSubTotal
            gettotalSubTotal = float(gettotalSellingPrice) - float(totalVAT)
            print(gettotalSubTotal)

            # For totalAmount
            print(gettotalSellingPrice)

            # For totalVATSale
            print(totalVATsale)

            # For status
            print('Pending')

            # For tableNo
            print(tableno)

            # For orderType
            print('DINE-IN')

            saveTempRestaurantOrderSummary = TempRestaurantOrderSummary(
                        referenceNo=refno,
                        totalItem=gettotalItem,
                        totalSellingPrice=gettotalSellingPrice,
                        totalTax=totalVAT,
                        totalQty=gettotalQty,
                        subTotal=gettotalSubTotal,
                        totalAmount=gettotalSellingPrice,
                        totalVATSale=totalVATsale,
                        preparedBy=request.user.username,
                        status='Pending',
                        tableNo=tableno,
                        orderType='DINE-IN'
                    )
            saveTempRestaurantOrderSummary.save()
            RestaurantTable.objects.filter(tableNo=tableno, isVat=False).update(tableStatus='Occupied', isVat=True)
    return redirect('restaurants:dines')

def cancelfoodmenu_view(request):
    if request.method == 'POST':
        refNo           = request.POST.get("refNo") 
        prodcode        = request.POST.get("prodCode") 
        tableno         = request.POST.get("tableNo")  

        TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, productCode=prodcode, tableNo=tableno, isVat=True).update(isCancelled=True, isVat=False, status='Cancelled')

    return HttpResponseRedirect('/restaurants/dine/'+tableno)

def editfoodmenu_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("id") 
        refno        = request.POST.get("ref") 
        qty         = request.POST.get("qty") 
        tableno         = request.POST.get("tableno") 

        try:
            getexists = TempRestaurantOrderDetail.objects.filter(referenceNo=refno, id=idno, isVat=True, isCancelled=False, tableNo=tableno,)
        except TempRestaurantOrderDetail.DoesNotExist:
            getexists = None
            raise Http404("No MyModel matches the given query.")

        if getexists is not None:
            for getexist in getexists:
                taxrate = 0.12
                gettotal = float(getexist.sellingPrice) * float(qty)
                updatesubtotal = float(gettotal) / 1.12
                updatetotaltax = updatesubtotal * taxrate

                TempRestaurantOrderDetail.objects.filter(referenceNo=refno, id=idno, isVat=True, isCancelled=False, tableNo=tableno,).update(qtySold=qty, totalAmount=gettotal, taxTotal=updatetotaltax, subTotal=updatesubtotal)
        return HttpResponseRedirect('/restaurants/dine/'+tableno)
    return HttpResponseRedirect('/restaurants/dine/'+tableno)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')