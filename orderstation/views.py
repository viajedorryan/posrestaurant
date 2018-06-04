from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from core.models import *
from . import views
import datetime
from django.db.models import Sum, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone
from .utils import render_to_pdf
from django.template.loader import get_template

from django.contrib.auth.decorators import login_required

import os, time

# Create your views here.
# function based view
# ORDERSTATION Section====================================================================================
def orderstation_view(request):
    # try:
    #     checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    # except SalesTransactionSummary.DoesNotExist:
    #     checks = None
    #     raise Http404("No MyModel matches the given query.")
    getlast = TempRestaurantOrderDetail.objects.last()
    print(getlast)
    tables = RestaurantTable.objects.all()
    template='orderstation_dine.html'
    context = {'tables':tables,'getlast':getlast}
    return render(request, template, context)
    # , 'successful_submit': True
# END ORDERSTATION Section=================================================================================


# ORDERSTATION DINE Section================================================================================
def orderdine_view(request):
    # try:
    #     checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    # except SalesTransactionSummary.DoesNotExist:
    #     checks = None
    #     raise Http404("No MyModel matches the given query.")
    tables = RestaurantTable.objects.all()
    template='orderstation_dine.html'
    context = {'tables':tables}
    return render(request, template, context)

def viewdine_view(request, tableNo, waiterID):
    
    getlast = TempRestaurantOrderDetail.objects.last()
    print(getlast)

    tables = RestaurantTable.objects.get(tableNo=tableNo)
    print(tables)

    waiters = Waiter.objects.get(waiterCode=waiterID)
    print(waiters)

    # Fetch all FoodMenu
    menus = FoodMenu.objects.filter(isVat=True)

    # Fetch all FoodCategory
    categories = FoodCategory.objects.filter(isVat=True)

    #Fetch all RestaurantOrderSummary that isVal=True
    countOrderSummaries = RestaurantOrderSummary.objects.count()
    print(countOrderSummaries)

    #Fetch all TempRestaurantOrderSummary that isVal=True
    countTempOrderSummaries = TempRestaurantOrderSummary.objects.count()
    totalTempOrderSummaries = countTempOrderSummaries + 1000

    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(referenceNo=totalTempOrderSummaries, tableNo=tables, isVat=True)

    tempOrderDetails = TempRestaurantOrderDetail.objects.filter(referenceNo=totalTempOrderSummaries, tableNo=tables, isVat=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(tempOrderDetails, 10)
    try:
        tempOrderDetailpages = paginator.page(page)
    except PageNotAnInteger:
        tempOrderDetailpages = paginator.page(1)
    except EmptyPage:
        tempOrderDetailpages = paginator.page(paginator.num_pages)
        

    template='ordertable.html'
    context = {'categories':categories,'tables': tables,'waiters': waiters,'tempOrderDetailpages': tempOrderDetailpages,'menus': menus,'totalTempOrderSummaries': totalTempOrderSummaries,'getOrderDetailsLists': getOrderDetailsLists,'getlast':getlast}
    return render(request, template, context)

def adddineorder_view(request):
    if request.method == 'POST':
        refNo           = request.POST.get("refNo") 
        prodcode        = request.POST.get("prodCode") 
        foodDesc        = request.POST.get("foodDesc")  
        foodSellPrice   = request.POST.get("foodSellPrice")  
        tableno         = request.POST.get("tableNo")  
        waiterName         = request.POST.get("waiterName")  
        waiterCode         = request.POST.get("waiterCode")  

        # getqty = float(foodSellPrice) *
        taxrate = 0.12
        subtotal = float(foodSellPrice) / 1.12
        totaltax = subtotal * taxrate

        try:
            getexists = TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, productCode=prodcode, tableNo=tableno, isVat=True, isCancelled=False)
        except TempRestaurantOrderDetail.DoesNotExist:
            getexists = None
            raise Http404("No MyModel matches the given query.")
        print(getexists)
        if not getexists:
            print('wal walawalalala')
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
                processedBy=waiterName,
                totalAmount=foodSellPrice,
                status='Pending',
                tableNo=tableno
            )
            saveTempRestaurantOrderDetail.save()
        if getexists:
            for getexist in getexists:
                print('naaaaaaaaaaaa')
                print(getexist)
                getqty = float(getexist.qtySold) + 1
                gettotal = float(getexist.sellingPrice) * getqty
                updatesubtotal = float(gettotal) / 1.12
                updatetotaltax = updatesubtotal * taxrate

                TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, productCode=prodcode, tableNo=tableno, isVat=True, isCancelled=False).update(qtySold=getqty, totalAmount=gettotal, taxTotal=updatetotaltax, subTotal=updatesubtotal)
    
    return HttpResponseRedirect('/orderstations/dine/'+tableno+'/'+waiterCode)

def savedineorder_view(request):
    if request.method == 'POST':
        refno           = request.POST.get("refNo")  
        tableno         = request.POST.get("tableNo")  
        waiterName         = request.POST.get("waiterName")  
        waiterCode         = request.POST.get("waiterCode")  
        print(refno)
        print(tableno)
        print(waiterName)
        print(waiterCode)
        # getOrderDetailsinfos = TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True)[:1].get()
        # print(getOrderDetailsinfos.referenceNo)try:
        try:
            getOrderDetailExists = TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True)
        except TempRestaurantOrderDetail.DoesNotExist:
            getOrderDetailExists = None
            raise Http404("No MyModel matches the given query.")

        print(getOrderDetailExists)

        if not getOrderDetailExists:
            messages.warning(request, 'Make sure the Order List Table is not Empty to proceed this Order.')
            return HttpResponseRedirect('/orderstations/dine/'+tableno+'/'+waiterCode)
        else:
            getOrderSummaryinfos =  TempRestaurantOrderSummary.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True)

            if getOrderSummaryinfos.exists():
                return HttpResponseRedirect('/orderstations/dine/'+tableno+'/'+waiterCode)
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
                            preparedBy=waiterName,
                            status='Pending',
                            tableNo=tableno,
                            orderType='DINE-IN'
                        )
                saveTempRestaurantOrderSummary.save()
                RestaurantTable.objects.filter(tableNo=tableno, isVat=False).update(tableStatus='Occupied', isVat=True)
    # return redirect('orderstations:orderstation')
    return HttpResponseRedirect('/orderstations/printorders/'+tableno+'/'+waiterCode)

def canceldineorder_view(request):
    if request.method == 'POST':
        refno           = request.POST.get("refNo")  
        tableno         = request.POST.get("tableNo")  
        waiterName         = request.POST.get("waiterName")  
        waiterCode         = request.POST.get("waiterCode") 
        print(refno)
        print(tableno)
        print(waiterName)
        print(waiterCode)

        TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, processedBy=waiterName, isVat=True).update(isCancelled=True, isVat=False, cancelledBy=waiterName, status='Cancelled')

    return redirect('orderstations:orderstation')

# END ORDERSTATION DINE Section============================================================================

# ORDERSTATION TAKEOUT Section=============================================================================
def ordertakeout_view(request, waiterID):
    try:
        getSalesTransactionSummaryExist = SalesTransactionSummary.objects.filter(isVat=True)
    except SalesTransactionSummary.DoesNotExist:
        getSalesTransactionSummaryExist = None
        raise Http404("No MyModel matches the given query.")
    print(getSalesTransactionSummaryExist)

    if not getSalesTransactionSummaryExist:
        messages.warning(request, 'The Cashier is OUT! Please inform the on Duty Cashier to Log In and Set a Cash Begin to proceed a Takeout Orders.')
        return redirect('orderstations:orderstation')
    else:
        try:
            getSalesTransactionSummary = SalesTransactionSummary.objects.get(isVat=True)
        except SalesTransactionSummary.DoesNotExist:
            getSalesTransactionSummary = None
            raise Http404("No MyModel matches the given query.")
        print(getSalesTransactionSummary)
        # Fetch all FoodMenu
        menus = FoodMenu.objects.filter(isVat=True)

        waiters = Waiter.objects.get(waiterCode=waiterID)
        print(waiters)

        # Fetch all FoodCategory
        categories = FoodCategory.objects.filter(isVat=True)

        #Fetch all RestaurantOrderSummary that isVal=True
        countOrderSummaries = RestaurantOrderSummary.objects.all().count()
        totalOrderSummaries = countOrderSummaries + 1000

        getOrderDetailsLists = RestaurantOrderDetail.objects.filter(orderNo=totalOrderSummaries)
        
        try:
            totalamount = RestaurantOrderDetail.objects.filter(isVat=False).aggregate(sum=Sum('totalAmount'))['sum']
        except RestaurantOrderDetail.DoesNotExist:
            totalamount = None
            raise Http404("No MyModel matches the given query.")

        if not totalamount:
            totalamount = 0
        totalVATsale = float(totalamount) / 1.12
        totalVAT = totalVATsale * 0.12
        
        try:
            totalitems = RestaurantOrderDetail.objects.filter(isVat=False).aggregate(sum=Sum('qtySold'))['sum']
        except RestaurantOrderDetail.DoesNotExist:
            totalitems = None
            raise Http404("No MyModel matches the given query.")
        if not totalitems:
            totalitems = 0

        tempOrderDetails = RestaurantOrderDetail.objects.filter(orderNo=totalOrderSummaries, isVat=False)
        page = request.GET.get('page', 1)

        paginator = Paginator(tempOrderDetails, 10)
        try:
            tempOrderDetailpages = paginator.page(page)
        except PageNotAnInteger:
            tempOrderDetailpages = paginator.page(1)
        except EmptyPage:
            tempOrderDetailpages = paginator.page(paginator.num_pages)
            
        template='orderstation_takeout.html'
        context = {'categories':categories, 'tempOrderDetailpages': tempOrderDetailpages,'menus': menus, 'totalOrderSummaries': totalOrderSummaries,'getSalesTransactionSummary': getSalesTransactionSummary,'getOrderDetailsLists': getOrderDetailsLists,'totalamount': totalamount,'totalitems': totalitems,'totalVATsale': totalVATsale,'totalVAT': totalVAT,'waiters': waiters}
        return render(request, template, context)
    return redirect('orderstations:ordertakeout')

def addordertakeout_view(request):
    if request.method == 'POST':
        orderno         = request.POST.get("orderNo") 
        transid         = request.POST.get("transID")  
        prodcode        = request.POST.get("prodCode") 
        foodDesc        = request.POST.get("foodDesc")  
        foodSellPrice   = request.POST.get("foodSellPrice")  
        waiterName         = request.POST.get("waiterName")  
        waiterCode         = request.POST.get("waiterCode")  

        # getqty = float(foodSellPrice) *
        taxrate = 0.12
        subtotal = float(foodSellPrice) / 1.12
        totaltax = subtotal * taxrate

        try:
            getexists = RestaurantOrderDetail.objects.filter(orderNo=orderno, productCode=prodcode, transactionCode=transid, isVat=False, isCancelled=False)
        except RestaurantOrderDetail.DoesNotExist:
            getexists = None
            raise Http404("No MyModel matches the given query.")
        print(getexists)
        if not getexists:
            print('wal walawalalala')
            RestaurantOrderDetail(
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
                        processedBy=waiterName,
                        totalAmount=foodSellPrice,
                        status='Pending'
                    ).save()
        if getexists:
            for getexist in getexists:
                print('naaaaaaaaaaaa')
                print(getexist)
                getqty = float(getexist.qtySold) + 1
                gettotal = float(getexist.sellingPrice) * getqty
                updatesubtotal = float(gettotal) / 1.12
                updatetotaltax = updatesubtotal * taxrate

                RestaurantOrderDetail.objects.filter(orderNo=orderno, productCode=prodcode, transactionCode=transid, isVat=False, isCancelled=False).update(qtySold=getqty, totalAmount=gettotal, taxTotal=updatetotaltax, subTotal=updatesubtotal)
    return HttpResponseRedirect('/orderstations/takeout/'+waiterCode)
    
# END ORDERSTATION TAKEOUT Section=========================================================================

# ORDERSTATION CHECKWAITER Section=========================================================================
def checkwaiter_view(request):
    answer     = request.POST.get("answer") 
    tableno     = request.POST.get("tableno") 
    print(answer)
    print(tableno)
    getwaitercode = Waiter.objects.filter(waiterCode=answer, isVat=True)

    if not getwaitercode:
        messages.warning(request, 'Please enter a correct CODE.')
        return redirect('orderstations:orderdine')
    if getwaitercode:
        return HttpResponseRedirect('/orderstations/dine/'+tableno+'/'+answer)
    # return redirect('orderstations:ordertakeout')

def checkwaitertakeout_view(request):
    answer     = request.POST.get("answer") 
    print(answer)
    getwaitercode = Waiter.objects.filter(waiterCode=answer, isVat=True)

    if not getwaitercode:
        messages.warning(request, 'Please enter a correct CODE.')
        return redirect('orderstations:orderdine')
    if getwaitercode:
        if request.user.is_authenticated:
            # return redirect('orderstations:ordertakeout')
            return HttpResponseRedirect('/orderstations/takeout/'+answer)
        else:
            messages.warning(request, 'The Cashier is OUT! Please inform the on Duty Cashier to Log In always in the main POS Machine to proceed ordering.')
            return redirect('orderstations:orderstation')
        # try:
        #     getSalesTransactionSummary = SalesTransactionSummary.objects.filter(isVat=True)
        # except SalesTransactionSummary.DoesNotExist:
        #     getSalesTransactionSummary = None
        #     raise Http404("No MyModel matches the given query.")
        # print(getSalesTransactionSummary)

        # if not getSalesTransactionSummary:
        #     messages.warning(request, 'The Cashier is OUT! Please inform the on Duty Cashier to Log In always in the main POS Machine to proceed ordering.')
        #     return redirect('orderstations:orderstation')
        # else:
        #     return redirect('orderstations:ordertakeout')
# END ORDERSTATION CHECKWAITER Section=====================================================================


# PRINTORDERS PDF Section==================================================================================
def printorders_view(request, tableNo, waiterID):
    dirname = 'C:/Users/RND-03/Documents/djangoprojects/posrestaurant/posrestaurant/web/static/Orders'
    if not os.path.exists(dirname):
        os.mkdir(os.path.join(dirname))

    possettings = POSSetting.objects.all()
    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(tableNo=tableNo, isVat=True, isCancelled=False)
    totalamount = TempRestaurantOrderDetail.objects.filter(tableNo=tableNo, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = TempRestaurantOrderDetail.objects.filter(tableNo=tableNo, isVat=True).aggregate(sum=Sum('qtySold'))['sum']

    print(getOrderDetailsLists)

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    today = timezone.now()
    params = {
            'possettings':possettings,
            'today': today,
            'tableno': tableNo,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'waiter': waiterID
        }
    for getOrderDetailsList in getOrderDetailsLists:
        filename = getOrderDetailsList.referenceNo

    pdf = render_to_pdf('printorders.html', params)
    response =  HttpResponse(pdf, content_type='application/pdf')
    filename = "Order_%s.pdf" %(filename)
    # filename = "Invoice.pdf"
    content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response
    # return redirect('orderstations:orderstation')
# END PRINTORDERS PDF Section==============================================================================