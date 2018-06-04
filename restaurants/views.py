from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from core.models import *
import datetime

from django.db.models import Sum, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# rest 
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.generic import View

from .utils import render_to_pdf
from django.template.loader import get_template

from django.utils import timezone
import os, csv
from pathlib import Path
import textwrap

from django.template import loader, Context

# Create your views here.
# function based view
# class GeneratePdf(View):
def generatePdf(request):   
    tableno         = request.POST.get("tableNo") 
    transcode       = request.POST.get("transCode") 
    orderno         = request.POST.get("orderNo") 
    
    possettings = POSSetting.objects.all()
    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True, isCancelled=False)
    totalamount = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True).aggregate(sum=Sum('qtySold'))['sum']

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    today = timezone.now()
    user = request.user.username
    params = {
            'possettings':possettings,
            'orderno':orderno,
            'today': today,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'user': user
        }
    return render_to_pdf('invoice.html', params)

    # ===================================================================

    # orderno         = request.POST.get("orderNo") 
    # transid         = request.POST.get("transID") 
    # print(orderno)
    # print(transid)
    # possettings = POSSetting.objects.all()
    # getitemlists =  RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=True)
    # totalamount = RestaurantOrderDetail.objects.filter(isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
    # totalitems = RestaurantOrderDetail.objects.filter(isVat=True).aggregate(sum=Sum('qtySold'))['sum']

    # if not totalamount:
    #     totalamount = 0
    # totalVATsale = float(totalamount) / 1.12
    # totalVAT = totalVATsale * 0.12

    # today = timezone.now()
    # user = request.user.username
    # print(getitemlists)
    # params = {
    #         'possettings':possettings,
    #         'orderno':orderno,
    #         'transno':transid,
    #         'today': today,
    #         'items': getitemlists,
    #         'totalamount': totalamount,
    #         'totalitems': totalitems,
    #         'totalVATsale': totalVATsale,
    #         'totalVAT': totalVAT,
    #         'user': user
    #     }
    # return render_to_pdf('invoice.html', params)
    # ====================================================================
    # template = get_template('invoice.html')
    # context = {
    #     "invoice_id": getitemlists.orderno,
    #     "customer_name": "John Cooper",
    #     "amount": getitemlists.transid,
    #     "today": "Today",
    # }
    # html = template.render(context)
    # pdf = render_to_pdf('invoice.html', context)
    # return HttpResponse(pdf, content_type='application/pdf')
    # if pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     # filename = "Invoice_%s.pdf" %("orderno")
    #     filename = "Invoice.pdf"
    #     content = "inline; filename='%s'" %(filename)
    #     download = request.GET.get("download")
    #     if download:
    #         content = "attachment; filename='%s'" %(filename)
    #     response['Content-Disposition'] = content
    #     return response
    # return HttpResponse("Not found")
@login_required(login_url="/accounts/login/")
def home_view(request):
    branches = Branch.objects.filter(isVat=True)
    print(request.user.id)
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    print(checks)
    
    template='home.html'
    context = {'branches': branches, 'checks': checks, 'time':datetime.date.today(), 'timezone':timezone.now()}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def cashin_view(request):
    if request.method == 'POST':
        code = request.POST.get('branchcode')
        name = request.POST.get('branchname')
        cashbegin = request.POST.get('cashbegin')
        user = request.user.id
        salessummary = SalesTransactionSummary.objects.all().count()

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

    return redirect('restaurants:dines')
    # template='home.html'
    # context = {}
    # return render(request, template, context)

@login_required(login_url="/accounts/login/")
def takeout_view(request):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")

    # Fetch all FoodMenu
    menus = FoodMenu.objects.filter(isVat=True)

    # Fetch all FoodCategory
    categories = FoodCategory.objects.filter(isVat=True)

    #Fetch all RestaurantOrderSummary that isVal=True
    countOrderSummaries = RestaurantOrderSummary.objects.all().count()
    totalOrderSummaries = countOrderSummaries + 1000

    getSalesTransactionSummary = SalesTransactionSummary.objects.get(userID=request.user.id, isVat=True)
    print(getSalesTransactionSummary)

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
        
    template='takeout.html'
    context = {'categories':categories,'checks':checks, 'tempOrderDetailpages': tempOrderDetailpages,'menus': menus, 'totalOrderSummaries': totalOrderSummaries,'getSalesTransactionSummary': getSalesTransactionSummary,'getOrderDetailsLists': getOrderDetailsLists,'totalamount': totalamount,'totalitems': totalitems,'totalVATsale': totalVATsale,'totalVAT': totalVAT}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
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
                        processedBy=request.user.username,
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
    return redirect('restaurants:takeout')

@login_required(login_url="/accounts/login/")
def edittakeoutfoodmenu_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("id") 
        orderno        = request.POST.get("ref") 
        qty         = request.POST.get("qty") 

        try:
            getexists = RestaurantOrderDetail.objects.filter(orderNo=orderno, id=idno, isVat=False, isCancelled=False)
        except TempRestaurantOrderDetail.DoesNotExist:
            getexists = None
            raise Http404("No MyModel matches the given query.")

        if getexists is not None:
            for getexist in getexists:
                taxrate = 0.12
                gettotal = float(getexist.sellingPrice) * float(qty)
                updatesubtotal = float(gettotal) / 1.12
                updatetotaltax = updatesubtotal * taxrate

                RestaurantOrderDetail.objects.filter(orderNo=orderno, id=idno, isVat=False, isCancelled=False).update(qtySold=qty, totalAmount=gettotal, taxTotal=updatetotaltax, subTotal=updatesubtotal)
        return redirect('restaurants:takeout')
    return redirect('restaurants:takeout')

@login_required(login_url="/accounts/login/")
def canceltakeoutfoodmenu_view(request):
    if request.method == 'POST':
        idno         = request.POST.get("idno") 
        print(idno)
        RestaurantOrderDetail.objects.filter(id=idno, isVat=False).update(isCancelled=True, isVat=True, status='Cancelled')

    return redirect('restaurants:takeout')

@login_required(login_url="/accounts/login/")
def paytakeoutfoodmenu_view(request):
    if request.method == 'POST':
        orderno         = request.POST.get("orderNo") 
        transid         = request.POST.get("transID")  
        amounttender    = request.POST.get("amounttender")
        amountpayable   = request.POST.get("amountpayable")
        
        controlno   = request.POST.get("controlno")
        seniorname   = request.POST.get("seniorname")
        othersdiscount   = request.POST.get("othersdiscount")

        if not controlno and not othersdiscount:
            discountType = 0
            seniorControlno = 0
            seniorName = 0
            totalDiscount = 0
            newamountpayable = amountpayable
            print('wala silang duha')

        if not controlno and othersdiscount:
            discountType = 'OTHERS'
            seniorControlno = 'OTHERS'
            seniorName = 'OTHERS'
            totalDiscount = float(othersdiscount)
            newamountpayable = float(amountpayable) - float(othersdiscount)
            print('naa si others')

        if controlno and not othersdiscount:
            discountType = 'SENIOR'
            seniorControlno = controlno
            seniorName = seniorname
            totalDiscount = 0.05 * float(amountpayable)
            newamountpayable = float(amountpayable) - float(totalDiscount)
            print('naa si senior')

        print(orderno)
        print(transid)
        print(amounttender)
        print(amountpayable)
        print(controlno)
        print(seniorname)
        print(othersdiscount)
        
        if float(amountpayable) > float(amounttender) or float(amountpayable) == 0:
            messages.warning(request, 'Tender Amount must not less than Amount Payable or Amount Payable must not equal to zero')
            return redirect('restaurants:takeout')
        else:
            getOrderSummaryinfos =  RestaurantOrderSummary.objects.filter(orderNo=orderno, transactionCode=transid, isVat=True)

            if getOrderSummaryinfos.exists():
                return redirect('restaurants:takeout')
            else:
                amountChange = float(amounttender) - float(newamountpayable)
                # amountChange = float(amounttender) - float(amountpayable)
                print(amountChange)
                
                # For orderNo
                print(orderno)

                # For transactionCode
                print(transid)

                # For totalItem
                gettotalItem = RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=False).aggregate(sum=Sum('qtySold'))['sum']
                print(gettotalItem)

                # For totalSellingPrice
                gettotalSellingPrice = RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=False).aggregate(sum=Sum('totalAmount'))['sum']
                print(gettotalSellingPrice)

                # For totalTax
                if not gettotalSellingPrice:
                    gettotalSellingPrice = 0
                totalVATsale = float(gettotalSellingPrice) / 1.12
                totalVAT = totalVATsale * 0.12
                print(totalVAT)

                # For totalQty
                gettotalQty = RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=False).aggregate(sum=Sum('qtySold'))['sum']
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
                            isVat=True,
                            amountTendered=amounttender,
                            amountChange=amountChange,
                            discountType=discountType,
                            seniorControlNo=seniorControlno,
                            seniorName=seniorName,
                            totalDiscount=totalDiscount
                        )
                saveOrderSummary.save()

                RestaurantOrderDetail.objects.filter(orderNo=orderno, transactionCode=transid, isVat=False).update(isVat=True, status='SOLD')
    
    # messages.success(request, 'Payment Success')
    template='sample.html'
    context = {'amounttender':amounttender,'amountChange':amountChange, 'successful_submit': True}
    return render(request, template, context)
    # return redirect('restaurants:takeout')

@login_required(login_url="/accounts/login/")
def dines_view(request):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    tables = RestaurantTable.objects.all()
    template='tables.html'
    context = {'checks':checks, 'tables': tables}
    return render(request, template, context)

def addamounttendered_view(request):
    if request.method == 'POST':
        cashremit           = request.POST.get("cashremit") 
        transcode           = request.POST.get("transcode") 

        RestaurantOrderSummary.objects.filter(accountCode=transcode, userID=request.user.id, isVat=True).update(cashRemitted=cashremit)

        return redirect('restaurants:closetransaction')

@login_required(login_url="/accounts/login/")
def payment_view(request):

    if request.method == 'POST':
        tableno         = request.POST.get("tableNo") 
        transcode       = request.POST.get("transCode") 
        orderno         = request.POST.get("orderNo") 
        amounttender    = request.POST.get("amounttender")
        amountpayable   = request.POST.get("amountpayable")
        
        controlno   = request.POST.get("controlno")
        seniorname   = request.POST.get("seniorname")
        othersdiscount   = request.POST.get("othersdiscount")

        if not controlno and not othersdiscount:
            discountType = 0
            seniorControlno = 0
            seniorName = 0
            totalDiscount = 0
            newamountpayable = amountpayable
            print('wala silang duha')

        if not controlno and othersdiscount:
            discountType = 'OTHERS'
            seniorControlno = 'OTHERS'
            seniorName = 'OTHERS'
            totalDiscount = float(othersdiscount)
            newamountpayable = float(amountpayable) - float(othersdiscount)
            print('naa si others')

        if controlno and not othersdiscount:
            discountType = 'SENIOR'
            seniorControlno = controlno
            seniorName = seniorname
            totalDiscount = 0.05 * float(amountpayable)
            newamountpayable = float(amountpayable) - float(totalDiscount)
            print('naa si senior')
        

        print(tableno)
        print(transcode)
        print(orderno)
        print(float(amounttender))
        print(amountpayable)
        print(controlno)
        print(seniorname)
        print(othersdiscount)

        if float(amountpayable) > float(amounttender):
            messages.warning(request, 'Tender Amount must not less than Amount Payable')
            return HttpResponseRedirect('/restaurants/billing/'+tableno)
        else:
            amountChange = float(amounttender) - float(newamountpayable)
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
                            isVat=True,
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
                        isVat=True,
                        amountTendered=amounttender,
                        amountChange=amountChange,
                        discountType=discountType,
                        seniorControlNo=seniorControlno,
                        seniorName=seniorName,
                        totalDiscount=totalDiscount
                    )
            saveOrderSummary.save()
            TempRestaurantOrderSummary.objects.filter(tableNo=tableno, isVat=True).update(isVat=False, status='SOLD')

            RestaurantTable.objects.filter(tableNo=tableno, isVat=True).update(isVat=False, tableStatus='Available')
    
    template='sample.html'
    context = {'amounttender':amounttender,'amountChange':amountChange, 'successful_submit': True}
    return render(request, template, context)
    # return redirect('restaurants:dines')

@login_required(login_url="/accounts/login/")
def billing_view(request, tableNo):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    tables = RestaurantTable.objects.get(tableNo=tableNo)
    print(tables)
    
    gettablelists = RestaurantTable.objects.filter(isVat=False)
    print(gettablelists)

    # Fetch all FoodMenu
    menus = FoodMenu.objects.filter(isVat=True)

    # Fetch all FoodCategory
    categories = FoodCategory.objects.filter(isVat=True)

    #Fetch all RestaurantOrderSummary that isVal=True
    countOrderSummaries = RestaurantOrderSummary.objects.count()
    print(countOrderSummaries)
    totalOrderSummaries = countOrderSummaries + 1000
    print(totalOrderSummaries)

    getSalesTransactionSummary = SalesTransactionSummary.objects.get(userID=request.user.id, isVat=True)
    print(getSalesTransactionSummary)

    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(tableNo=tables, isVat=True, isCancelled=False)

    getOrdernos = TempRestaurantOrderDetail.objects.filter(tableNo=tables, isVat=True, isCancelled=False)
    print('===========================================')
    for ordernum in getOrdernos:
        getOrderno = ordernum.referenceNo
        print(ordernum.referenceNo)
        print('===========================================')

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
    context = {'categories':categories,'checks':checks,'tables': tables,'menus': menus,'totalOrderSummaries': totalOrderSummaries,'getSalesTransactionSummary': getSalesTransactionSummary,'tempOrderDetailpages':tempOrderDetailpages,'totalamount': totalamount,'totalitems': totalitems,'totalVATsale': totalVATsale,'totalVAT': totalVAT,'getOrderno': getOrderno, 'gettablelists':gettablelists}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def dine_view(request, tableNo):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    tables = RestaurantTable.objects.get(tableNo=tableNo)
    print(tables)

    # Fetch all FoodMenu
    menus = FoodMenu.objects.filter(isVat=True)

    # Fetch all FoodCategory
    categories = FoodCategory.objects.filter(isVat=True)

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
    context = {'categories':categories,'checks':checks,'tables': tables,'tempOrderDetailpages': tempOrderDetailpages,'menus': menus,'totalTempOrderSummaries': totalTempOrderSummaries,'totalOrderSummaries': totalOrderSummaries,'getSalesTransactionSummary': getSalesTransactionSummary,'getOrderDetailsLists': getOrderDetailsLists,'totalamount': totalamount,'totalitems': totalitems,'totalVATsale': totalVATsale,'totalVAT': totalVAT}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
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
                processedBy=request.user.username,
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

        # saveTempRestaurantOrderDetail = TempRestaurantOrderDetail(
        #             referenceNo=refNo,
        #             productCode=prodcode,
        #             branchCode=888,
        #             description=foodDesc,
        #             sellingPrice=foodSellPrice,
        #             qtySold=1,
        #             unitMeasure='kg',
        #             taxRate=taxrate,
        #             taxTotal=totaltax,
        #             subTotal=subtotal,
        #             processedBy=request.user.username,
        #             totalAmount=foodSellPrice,
        #             status='Pending',
        #             tableNo=tableno
        #         )
        # saveTempRestaurantOrderDetail.save()
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

@login_required(login_url="/accounts/login/")
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
    # return HttpResponseRedirect('/restaurants/downloaddine/'+tableno+'/'+refno)

@login_required(login_url="/accounts/login/")
def cancelfoodmenu_view(request):
    if request.method == 'POST':
        idno         = request.POST.get("idno") 
        # refNo           = request.POST.get("refNo") 
        # prodcode        = request.POST.get("prodCode") 
        tableno         = request.POST.get("tableNo")  

        TempRestaurantOrderDetail.objects.filter(id=idno, isVat=True).update(isCancelled=True, isVat=False, cancelledBy=request.user.username, status='Cancelled')

    return HttpResponseRedirect('/restaurants/dine/'+tableno)

@login_required(login_url="/accounts/login/")
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

def cancelbillfoodmenu_view(request):
    if request.method == 'POST':
        idno         = request.POST.get("idno") 
        # refNo           = request.POST.get("refNo") 
        # prodcode        = request.POST.get("prodCode") 
        tableno         = request.POST.get("tableNo")  
        print(idno)
        print(tableno)
        TempRestaurantOrderDetail.objects.filter(id=idno, isVat=True).update(isCancelled=True, isVat=False, cancelledBy=request.user.username, status='Cancelled')

    return HttpResponseRedirect('/restaurants/billing/'+tableno)

@login_required(login_url="/accounts/login/")
def editbillfoodmenu_view(request):
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
        
        getOrderSummaryinfos =  TempRestaurantOrderSummary.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True)

        if getOrderSummaryinfos.exists():
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

            TempRestaurantOrderSummary.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True).update(totalItem=gettotalItem,totalSellingPrice=gettotalSellingPrice,totalTax=totalVAT,totalQty=gettotalQty,subTotal=gettotalSubTotal,totalAmount=gettotalSellingPrice,totalVATSale=totalVATsale,)
        else:
            return HttpResponseRedirect('/restaurants/billing/'+tableno)
    return HttpResponseRedirect('/restaurants/billing/'+tableno)

@login_required(login_url="/accounts/login/")
def addbillfoodmenu_view(request):
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

        print(refNo)

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
                processedBy=request.user.username,
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

        # try:
        #     getexists = TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, productCode=prodcode, tableNo=tableno, isVat=True, isCancelled=False)
        # except TempRestaurantOrderDetail.DoesNotExist:
        #     getexists = None
        #     raise Http404("No MyModel matches the given query.")
        # print(getexists)
        # if getexists is None:
        # getexists = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True)


        # saveTempRestaurantOrderDetail = TempRestaurantOrderDetail(
        #             referenceNo=refNo,
        #             productCode=prodcode,
        #             branchCode=888,
        #             description=foodDesc,
        #             sellingPrice=foodSellPrice,
        #             qtySold=1,
        #             unitMeasure='kg',
        #             taxRate=taxrate,
        #             taxTotal=totaltax,
        #             subTotal=subtotal,
        #             processedBy=request.user.username,
        #             totalAmount=foodSellPrice,
        #             status='Pending',
        #             tableNo=tableno
        #         )
        # saveTempRestaurantOrderDetail.save()
        # return HttpResponseRedirect('/restaurants/table/'+tableno)
        # if getexists is not None:
        #     for getexist in getexists:
        #         plusqty = float(getexist.qtySold) + 1
        #         gettotal = float(foodSellPrice) * plusqty
        #         updatesubtotal = float(gettotal) / 1.12
        #         updatetotaltax = updatesubtotal * taxrate

        #         TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, productCode=prodcode, tableNo=tableno, isVat=True).update(qtySold=plusqty, totalAmount=gettotal, taxTotal=updatetotaltax, subTotal=updatesubtotal)
        #         return HttpResponseRedirect('/restaurants/table/'+tableno)
        getOrderSummaryinfos =  TempRestaurantOrderSummary.objects.filter(referenceNo=refNo, tableNo=tableno, isVat=True)

        if getOrderSummaryinfos.exists():
            # For totalItem
            gettotalItem = TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, tableNo=tableno, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
            print(gettotalItem)

            # For totalSellingPrice
            gettotalSellingPrice = TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, tableNo=tableno, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
            print(gettotalSellingPrice)

            # For totalTax
            if not gettotalSellingPrice:
                gettotalSellingPrice = 0
            totalVATsale = float(gettotalSellingPrice) / 1.12
            totalVAT = totalVATsale * 0.12
            print(totalVAT)

            # For totalQty
            gettotalQty = TempRestaurantOrderDetail.objects.filter(referenceNo=refNo, tableNo=tableno, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
            print(gettotalQty)

            # For totalSubTotal
            gettotalSubTotal = float(gettotalSellingPrice) - float(totalVAT)
            print(gettotalSubTotal)

            TempRestaurantOrderSummary.objects.filter(referenceNo=refNo, tableNo=tableno, isVat=True).update(totalItem=gettotalItem,totalSellingPrice=gettotalSellingPrice,totalTax=totalVAT,totalQty=gettotalQty,subTotal=gettotalSubTotal,totalAmount=gettotalSellingPrice,totalVATSale=totalVATsale,)
        else:
            return HttpResponseRedirect('/restaurants/billing/'+tableno)

    return HttpResponseRedirect('/restaurants/billing/'+tableno)

# Sales Section====================================================================================
@login_required(login_url="/accounts/login/")
def sales_view(request):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    getpendingsales = TempRestaurantOrderSummary.objects.filter(isVat=True, preparedBy=request.user.username)
    getsoldsales = RestaurantOrderSummary.objects.filter(isVoid=False, isCancelled=False, isHold=False, isVat=True, preparedBy=request.user.username)
    template='sales.html'
    context = {'checks':checks,'getsoldsales':getsoldsales, 'getpendingsales':getpendingsales}
    return render(request, template, context)
# END Sales Section================================================================================

# Table Section====================================================================================
@login_required(login_url="/accounts/login/")
def tablelist_view(request):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    gettablelists = RestaurantTable.objects.all()
    template='tablelist.html'
    context = {'checks':checks,'gettablelists':gettablelists}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def addtable_view(request):
    if request.method == 'POST':
        tableno           = request.POST.get("tableno") 

        RestaurantTable(
                tableNo=tableno,
                addedBy=request.user.username
            ).save()
        return redirect('restaurants:tablelist')

@login_required(login_url="/accounts/login/")
def edittable_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("idno") 
        tableno           = request.POST.get("tableno") 

        RestaurantTable.objects.filter(id=idno).update(tableNo=tableno)
        return redirect('restaurants:tablelist')
@login_required(login_url="/accounts/login/")
def deletetable_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("idno") 

        RestaurantTable.objects.get(pk=idno).delete()
        return redirect('restaurants:tablelist')
# END Table Section=================================================================================

# Food Menu Section=================================================================================
@login_required(login_url="/accounts/login/")
def foodmenulist_view(request):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    getmenulists = FoodMenu.objects.filter(isVat=True)
    getcategorylists = FoodCategory.objects.filter(isVat=True)
    template='foodmenulist.html'
    context = {'checks':checks,'getmenulists':getmenulists,'getcategorylists':getcategorylists}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def addfoodmenulist_view(request):
    if request.method == 'POST':
        menu           = request.POST.get("menu") 
        category       = request.POST.get("category") 
        price       = request.POST.get("price") 
        print(menu)
        print(category)
        print(price)

        getcategorylists = FoodCategory.objects.filter(categoryName=category)

        for getcategorylist in getcategorylists:
            catid = getcategorylist.id * 1000
            print(catid)
            countmain = FoodMenu.objects.filter(menuCategory=category).count()
            print(countmain)
            foodcode = catid + countmain
            print(foodcode)
            FoodMenu(
                    foodCode=foodcode,
                    foodMenu=menu,
                    menuCategory=category,
                    price=price
                ).save()

            # if category == getcategorylist.categoryName:
            #     getmains = FoodCategory.objects.filter(categoryName=category)
            #     print(getmains)
            #     for getmain in getmains:
            #         countmain = FoodMenu.objects.filter(menuCategory=getmain.categoryName).count()
            #         print(countmain)
            #         mainfoodcode = countmain + 1000
            #         print(mainfoodcode)
            #         FoodMenu(
            #                 foodCode=mainfoodcode,
            #                 foodMenu=menu,
            #                 menuCategory=category,
            #                 price=price
            #             ).save()


        # if category == 'SOUPS':
        #     getsoups = FoodCategory.objects.filter(categoryName=category)
        #     print(getsoups)
        #     for getsoup in getsoups:
        #         countmain = FoodMenu.objects.filter(menuCategory=getsoup.categoryName).count()
        #         print(countmain)
        #         soupfoodcode = countmain + 2000
        #         print(soupfoodcode)
        #         FoodMenu(
        #                 foodCode=soupfoodcode,
        #                 foodMenu=menu,
        #                 menuCategory=category,
        #                 price=price
        #             ).save()

        # if category == 'BEVERAGES':
        #     getbeves = FoodCategory.objects.filter(categoryName=category)
        #     print(getbeves)
        #     for getbeve in getbeves:
        #         countmain = FoodMenu.objects.filter(menuCategory=getbeve.categoryName).count()
        #         print(countmain)
        #         bevefoodcode = countmain + 3000
        #         print(bevefoodcode)
        #         FoodMenu(
        #                 foodCode=bevefoodcode,
        #                 foodMenu=menu,
        #                 menuCategory=category,
        #                 price=price
        #             ).save()

    return redirect('restaurants:foodmenulist')

@login_required(login_url="/accounts/login/")
def editfoodmenulist_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("idno") 
        price           = request.POST.get("price") 

        FoodMenu.objects.filter(id=idno).update(price=price)
        return redirect('restaurants:foodmenulist')

@login_required(login_url="/accounts/login/")
def deletefoodmenulist_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("idno") 

        FoodMenu.objects.filter(id=idno).update(isVat=False)
        return redirect('restaurants:foodmenulist')
# END Food Menu Section=============================================================================

# Close Transaction Section=========================================================================
@login_required(login_url="/accounts/login/")
def closetransaction_view(request):

    gettransactioncode = SalesTransactionSummary.objects.get(userID=request.user.id,isVat=True)
    print(gettransactioncode)

    gettotalcash = RestaurantOrderSummary.objects.filter(transactionCode=gettransactioncode,preparedBy=request.user.username, isVat=True, isVoid=False, isCancelled=False, isHold=False).aggregate(sum=Sum('totalUnitPrice'))['sum']
    print(gettotalcash)

    gettotalqty = RestaurantOrderSummary.objects.filter(transactionCode=gettransactioncode,preparedBy=request.user.username, isVat=True, isVoid=False, isCancelled=False, isHold=False).aggregate(sum=Sum('totalQty'))['sum']
    print(gettotalqty)

    getsalesinfos = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=True)
    for getsalesinfo in getsalesinfos:
            cashinhand = getsalesinfo.beginningCash
            timeopen = getsalesinfo.date_created
            if getsalesinfo.cashRemitted is None:
                cashremit = 0
            else:
                cashremit = getsalesinfo.cashRemitted
    if cashremit:
        getdifferences = cashremit - gettotalcash
    else:
        getdifferences = 0

    template='closetransaction.html'
    context = {'cashinhand':cashinhand,'timeopen':timeopen,'gettotalcash':gettotalcash,'gettransactioncode':gettransactioncode,'cashremit':cashremit,'getdifferences':getdifferences,'gettotalqty':gettotalqty}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def addcashremit_view(request):
    if request.method == 'POST':
        cashremit           = request.POST.get("cashremit") 
        transcode           = request.POST.get("transcode") 

        SalesTransactionSummary.objects.filter(accountCode=transcode, userID=request.user.id, isVat=True).update(cashRemitted=cashremit)

        return redirect('restaurants:closetransaction')
@login_required(login_url="/accounts/login/")
def closed_view(request):
    if request.method == 'POST':
        transcode           = request.POST.get("transcode") 
        totalcash           = request.POST.get("totalcash") 
        shortage           = request.POST.get("shortage") 
        totalqty           = request.POST.get("totalqty") 

        SalesTransactionSummary.objects.filter(accountCode=transcode, userID=request.user.id, isVat=True).update(totalCashSales=totalcash,totalCash=totalcash,noOfSoldItem=totalqty,totalSoldItem=totalqty,shortage=shortage,closedBy=request.user.id,isVat=False)

        RestaurantOrderSummary.objects.filter(transactionCode=transcode, isVat=False).update(isVat=True)

    return redirect('restaurants:home')
# END Close Transaction Section=====================================================================

# VOID Section======================================================================================
@login_required(login_url="/accounts/login/")
def void_view(request):
    try:
        getvoidlists = RestaurantOrderDetail.objects.filter(isCancelled=False, isVoid=False, isHold=False, isVat=True)
    except RestaurantOrderDetail.DoesNotExist:
        getvoidlists = None
        raise Http404("No MyModel matches the given query.")

    template='void.html'
    context = {'getvoidlists':getvoidlists}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def voidmenu_view(request):
    if request.method == 'POST':
        orderNo        = request.POST.get("orderNo")  
        idno           = request.POST.get("idno")  
        print(orderNo)
        RestaurantOrderDetail.objects.filter(id=idno, orderNo=orderNo, isVat=True).update(isErrorCorrect=True, isVoid=True, voidBy=request.user.username, status='VOID')

        # For totalItem
        gettotalItem = RestaurantOrderDetail.objects.filter(orderNo=orderNo).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalItem)

        # For totalItemSold
        gettotalItemSold = RestaurantOrderDetail.objects.filter(orderNo=orderNo, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalItemSold)

        # For totalSellingPrice
        gettotalSellingPrice = RestaurantOrderDetail.objects.filter(orderNo=orderNo, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
        print(gettotalSellingPrice)

        # For totalTax
        if not gettotalSellingPrice:
            gettotalSellingPrice = 0
        totalVATsale = float(gettotalSellingPrice) / 1.12
        totalVAT = totalVATsale * 0.12
        print(totalVAT)

        # For totalQty
        gettotalQty = RestaurantOrderDetail.objects.filter(orderNo=orderNo, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalQty)

        # For totalSubTotal
        gettotalSubTotal = float(gettotalSellingPrice) - float(totalVAT)
        print(gettotalSubTotal)

        # For totalAmount
        print(gettotalSellingPrice)

        # For totalVATSale
        print(totalVATsale)

        # For totalItemCancelled
        gettotalItemCancelled = RestaurantOrderDetail.objects.filter(orderNo=orderNo, isCancelled=True, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalItemCancelled)
        if not gettotalItemCancelled:
            gettotalItemCancelled = 0
            print(gettotalItemCancelled)

        # For totalItemVoid
        gettotalItemVoid = RestaurantOrderDetail.objects.filter(orderNo=orderNo, isVoid=True, isErrorCorrect=True, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalItemVoid)
        if not gettotalItemVoid:
            gettotalItemVoid = 0
            print(gettotalItemVoid)

        getamountTendered =  RestaurantOrderSummary.objects.filter(orderNo=orderNo, isVat=True).aggregate(sum=Sum('amountTendered'))['sum']
        print(getamountTendered)

        amountChange = float(getamountTendered) - float(gettotalSellingPrice)
        print(amountChange)

        RestaurantOrderSummary.objects.filter(orderNo=orderNo, isVat=True).update(totalItem=gettotalItem, totalItemSold=gettotalItemSold, totalSellingPrice=gettotalSellingPrice, totalTax=totalVAT, totalQty=gettotalQty, subTotal=gettotalSubTotal, totalAmount=gettotalSellingPrice, totalVATSale=totalVATsale, totalItemCancelled=gettotalItemCancelled, totalItemVoid=gettotalItemVoid, totalUnitPrice=gettotalSellingPrice, amountChange=amountChange, voidBy=request.user.username)

    return redirect('restaurants:void')
# END VOID Section==================================================================================

# TRANSACTION VOID Section==========================================================================
@login_required(login_url="/accounts/login/")
def transvoidfoodmenu_view(request):
    if request.method == 'POST':
        refno           = request.POST.get("refNo")  
        tableno         = request.POST.get("tableNo")  
        print(refno)
        print(tableno)

        TempRestaurantOrderDetail.objects.filter(referenceNo=refno, tableNo=tableno, isVat=True).update(isVoid=True, isVat=False, voidBy=request.user.username, status='VOID')

    return redirect('restaurants:dines')

@login_required(login_url="/accounts/login/")
def takeouttransvoidfoodmenu_view(request):
    if request.method == 'POST':
        refno           = request.POST.get("refNo")  
        transcode           = request.POST.get("transCode")  
        print(refno)

        RestaurantOrderDetail.objects.filter(orderNo=refno, isVat=False).update(isVoid=True, isVat=True, voidBy=request.user.username, status='VOID')

        # For totalItem
        gettotalItem = RestaurantOrderDetail.objects.filter(orderNo=refno, transactionCode=transcode).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalItem)

        # For totalItemSold
        gettotalItemSold = RestaurantOrderDetail.objects.filter(orderNo=refno, transactionCode=transcode, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalItemSold)

        # For totalSellingPrice
        gettotalSellingPrice = RestaurantOrderDetail.objects.filter(orderNo=refno, transactionCode=transcode, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
        print(gettotalSellingPrice)

        # For totalTax
        if not gettotalSellingPrice:
            gettotalSellingPrice = 0
        totalVATsale = float(gettotalSellingPrice) / 1.12
        totalVAT = totalVATsale * 0.12
        print(totalVAT)

        # For totalQty
        gettotalQty = RestaurantOrderDetail.objects.filter(orderNo=refno, transactionCode=transcode, isVat=True).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalQty)

        # For totalSubTotal
        gettotalSubTotal = float(gettotalSellingPrice) - float(totalVAT)
        print(gettotalSubTotal)

        # For totalItemVoid
        gettotalItemVoid = RestaurantOrderDetail.objects.filter(orderNo=refno, isVoid=True, isErrorCorrect=True, isVat=False).aggregate(sum=Sum('qtySold'))['sum']
        print(gettotalItemVoid)
        if not gettotalItemVoid:
            gettotalItemVoid = 0
            print(gettotalItemVoid)

        RestaurantOrderSummary(
                    orderNo=refno,
                    transactionCode=transcode,
                    totalItem=gettotalItem,
                    totalItemSold=gettotalItem,
                    totalSellingPrice=gettotalSellingPrice,
                    totalUnitPrice=gettotalSellingPrice,
                    totalTax=totalVAT,
                    totalQty=gettotalQty,
                    subTotal=gettotalSubTotal,
                    totalAmount=gettotalSellingPrice,
                    totalVATSale=totalVATsale,
                    totalItemVoid=gettotalItemVoid,
                    voidBy=request.user.username,
                    isVoid=True,
                    status='VOID',
                    orderType='TAKEOUT',
                    isVat=True
                ).save()

    return redirect('restaurants:takeout')
# END TRANSACTION VOID Section======================================================================

# Food Category Section=============================================================================
@login_required(login_url="/accounts/login/")
def foodcategorylist_view(request):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    getmenulists = FoodMenu.objects.filter(isVat=True)
    getcategorylists = FoodCategory.objects.filter(isVat=True)
    template='foodcategorylist.html'
    context = {'checks':checks,'getmenulists':getmenulists,'getcategorylists':getcategorylists}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def addfoodcategorylist_view(request):
    if request.method == 'POST':
        category       = request.POST.get("category") 
        print(category)

        getcategories = FoodCategory.objects.filter(categoryName=category)

        if getcategories.exists():
            return redirect('restaurants:foodcategorylist')
        else:
            FoodCategory(
                categoryName=category,
                isVat=True
            ).save()
    return redirect('restaurants:foodcategorylist')

@login_required(login_url="/accounts/login/")
def editfoodcategorylist_view(request):
    if request.method == 'POST':
        idno               = request.POST.get("idno") 
        category           = request.POST.get("category") 

        FoodCategory.objects.filter(id=idno).update(categoryName=category)
        return redirect('restaurants:foodcategorylist')

@login_required(login_url="/accounts/login/")
def deletefoodcategorylist_view(request):
    if request.method == 'POST':
        idno           = request.POST.get("idno") 

        FoodCategory.objects.filter(id=idno).update(isVat=False)
        return redirect('restaurants:foodcategorylist')
# END Food Category Section=========================================================================

# POS SETTINGS Section==============================================================================
@login_required(login_url="/accounts/login/")
def possettings_view(request):
    possettings = POSSetting.objects.all()
    print(request.user.id)
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    print(checks)
    template='possettings.html'
    context = {'possettings': possettings, 'checks': checks, 'time':datetime.date.today()}
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def editpossettings_view(request):
    if request.method == 'POST':
        branchcode      = request.POST.get("branchcode") 
        companyname     = request.POST.get("companyname") 
        addone          = request.POST.get("addone")     
        addtwo          = request.POST.get("addtwo") 
        tinno           = request.POST.get("tinno") 
        minno           = request.POST.get("minno") 
        birno           = request.POST.get("birno") 
        serialno        = request.POST.get("serialno") 

        POSSetting.objects.filter(branchCode=branchcode).update(companyName=companyname,address1=addone,address2=addtwo,tinNo=tinno,minNo=minno,birPermitNo=birno,serialNo=serialno)
    messages.success(request, 'POS Settings Updated Successfully!')
    return redirect('restaurants:possettings')
# END POS SETTINGS Section==========================================================================

# GENERATE RECEIPT Section==========================================================================
@login_required(login_url="/accounts/login/")
def generateBill(request):   

    
    # papersize = 76
    # papersize1 = 38
    # # msg = 'ryan viajedor'
    # # for i in msg:
    # #     print(i, end='')
    # # print('')
    # # string2="Ryan M. Viajedor"
    # # # string_length=len(string2)+10    # will be adding 10 extra spaces
    # # # string_revised=string2.rjust(string_length)
    # # # print (string_revised)
    # # minusSTR1 = papersize1 - (len(string2)/2) + len(string2)
    # # print(minusSTR1)
    # # print(string2.rjust(int(minusSTR1), '0'))
    # # minusSTR = papersize -len(string2)
    # # print(minusSTR)
    # # divideSTR = minusSTR / 2
    # # print(divideSTR)
    # # print(string2.rjust(int(divideSTR), '0') + minusSTR1)



    # dirname = 'C:/POSTransaction/Restaurant/Billing/'
    # if not os.path.exists(dirname):
    #     os.mkdir(os.path.join(dirname))

    # player = 'bob'

    # filename = dirname+player+'.txt'

    # if os.path.exists(filename):
    #     append_write = 'a' # append if already exists
    # else:
    #     append_write = 'w' # make a new file if not
    # possettings = POSSetting.objects.all()
    # for possetting in possettings:
        
    #     doCompanyName = papersize1 - (len(possetting.companyName)/2)
    #     print(doCompanyName)
    #     companyName = possetting.companyName.rjust(int(doCompanyName)+len(possetting.companyName), ' ')
    #     print(len(companyName))

    #     doAddress = papersize1 - (len(possetting.address1)/2)
    #     address1 = possetting.address1.rjust(int(doAddress)+len(possetting.address1), ' ')
        

    #     cntTIN = 'TIN:'+possetting.tinNo
    #     doTinNo = papersize1 - (len(cntTIN)/2)
    #     tinNo = cntTIN.rjust(int(doTinNo)+len(cntTIN), ' ')

    #     print(companyName)
    #     print(address1)
    #     print(tinNo)

    #     cntMIN = 'MIN #:'+possetting.minNo
    #     doMinNo = papersize1 - (len(cntMIN)/2)
    #     minNo = cntMIN.rjust(int(doMinNo)+len(cntMIN), ' ')
        
    #     cntBIR = 'BIR PERMIT #:'+possetting.birPermitNo
    #     doBirPermitNo = papersize1 - (len(cntBIR)/2)
    #     birPermitNo = cntBIR.rjust(int(doBirPermitNo)+len(cntBIR), ' ')
        
    #     cntSN = 'S/N:'+possetting.serialNo
    #     doSerialNo = papersize1 - (len(cntSN)/2)
    #     serialNo = cntSN.rjust(int(doSerialNo)+len(cntSN), ' ')

    #     highscore = open(filename,append_write)
    #     highscore.write(companyName + '\n')
    #     highscore.write(address1 + '\n')
    #     highscore.write(tinNo + '\n')
    #     highscore.write(serialNo + '\n')
    #     highscore.write(birPermitNo + '\n')
    #     highscore.write(minNo + '\n')
    #     highscore.close()
        
    # os.startfile("C:/POSTransaction/Restaurant/Billing/bob.txt", "print")
    # =================================
    tableno         = request.POST.get("tableNo") 
    transcode       = request.POST.get("transCode") 
    orderno         = request.POST.get("orderNo") 
    
    possettings = POSSetting.objects.all()
    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True, isCancelled=False)
    totalamount = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True).aggregate(sum=Sum('qtySold'))['sum']

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    today = timezone.now()
    user = request.user.username
    params = {
            'possettings':possettings,
            'orderno':orderno,
            'today': today,
            'tableno': tableno,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'user': user
        }

    return render_to_pdf('bill.html', params)
    # ===================================================
    # os.startfile("C:/POSTransaction/Restaurant/Billing/10001.txt", "print")
    # print('==================================================')
    # print(os.getcwd())
    # pdf = render_to_pdf('bill.html', params)
    # response =  HttpResponse(pdf, content_type='application/pdf')
    # filename = "Billing_%s.pdf" %(orderno)
    # # filename = "Invoice.pdf"
    # content = "attachment; filename='%s'" %(filename)
    # response['Content-Disposition'] = content
    # return response

     

@login_required(login_url="/accounts/login/")
def generate_bill(request):
    tableno         = request.POST.get("tableNo") 
    orderno         = request.POST.get("orderNo") 

    possettings = POSSetting.objects.all()
    getOrderDetailsLists = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False)
    totalamount = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('qtySold'))['sum']

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    if not tableno:
        tableno = 'TAKEOUT'

    today = timezone.now()
    user = request.user.username
    params = {
            'possettings':possettings,
            'orderno':orderno,
            'today': today,
            'tableno': tableno,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'user': user
        }

    return render_to_pdf('bill.html', params)

@login_required(login_url="/accounts/login/")
def generateReceipt(request):
    tableno         = request.POST.get("tableNo") 
    orderno         = request.POST.get("orderNo") 

    possettings = POSSetting.objects.all()
    getOrderDetailsLists = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False)
    totalamount = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('qtySold'))['sum']
    cash = RestaurantOrderSummary.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('amountTendered'))['sum']
    change = RestaurantOrderSummary.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('amountChange'))['sum']
    totaldiscounts = RestaurantOrderSummary.objects.filter(orderNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('totalDiscount'))['sum']

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    if not tableno:
        tableno = 'TAKEOUT'

    today = timezone.now()
    user = request.user.username
    params = {
            'possettings':possettings,
            'orderno':orderno,
            'today': today,
            'tableno': tableno,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'cash': cash,
            'change': change,
            'user': user,
            'totaldiscounts':totaldiscounts
        }

    return render_to_pdf('receipt.html', params)

# END GENERATE RECEIPT Section======================================================================

# REPORTS Section===================================================================================
@login_required(login_url="/accounts/login/")
def reports_view(request):
    try:
        checks = SalesTransactionSummary.objects.filter(userID=request.user.id, isVat=1).count()
    except SalesTransactionSummary.DoesNotExist:
        checks = None
        raise Http404("No MyModel matches the given query.")
    print(checks)

    try:
        getsolds = RestaurantOrderDetail.objects.filter(status='SOLD').aggregate(sum=Sum('qtySold'))['sum']
    except RestaurantOrderDetail.DoesNotExist:
        getsolds = None
        raise Http404("No MyModel matches the given query.")
    if not getsolds:
        getsolds = 0
    print(getsolds)

    try:
        getvoids = RestaurantOrderDetail.objects.filter(status='VOID').aggregate(sum=Sum('qtySold'))['sum']
    except RestaurantOrderDetail.DoesNotExist:
        getvoids = None
        raise Http404("No MyModel matches the given query.")
    if not getvoids:
        getvoids = 0
    print(getvoids)

    try:
        getcancelled = RestaurantOrderDetail.objects.filter(status='Cancelled').aggregate(sum=Sum('qtySold'))['sum']
    except RestaurantOrderDetail.DoesNotExist:
        getcancelled = None
        raise Http404("No MyModel matches the given query.")
    if not getcancelled:
        getcancelled = 0
    print(getcancelled)
    getsales = RestaurantOrderSummary.objects.all().count()
    print(getsales)
    gettakeouts = RestaurantOrderSummary.objects.filter(orderType='TAKEOUT').count()
    print(gettakeouts)
    getdineins = RestaurantOrderSummary.objects.filter(orderType='DINE-IN').count()
    print(getdineins)


    template='reports.html'
    context = {'checks': checks,'getsales': getsales,'getsolds': getsolds,'getvoids': getvoids,'getcancelled': getcancelled,'gettakeouts': gettakeouts,'getdineins': getdineins}
    return render(request, template, context)

class SalesChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        c = []
        t = []
        for sales in RestaurantOrderSummary.objects.values('date_created').distinct():
            # print(country)
            for key, value in sales.items():
                # print(value)
                total = RestaurantOrderSummary.objects.filter(totalUnitPrice=value).count()
                # print(total)
                c.append(value)
                t.append(total)

        labels = c
        items = t
        data = {
            "labels": labels,
            "default": items,
        }
        return Response(data)
# END REPORTS Section===============================================================================

# TRANSFER TABLE Section============================================================================
@login_required(login_url="/accounts/login/")
def transfertable_view(request):
    if request.method == 'POST':
        fromtable               = request.POST.get("fromtable") 
        totable           = request.POST.get("totable") 
        print(fromtable)
        print(totable)

        TempRestaurantOrderDetail.objects.filter(tableNo=fromtable, isVat=True).update(tableNo=totable)
        TempRestaurantOrderSummary.objects.filter(tableNo=fromtable, isVat=True).update(tableNo=totable)
        RestaurantTable.objects.filter(tableNo=fromtable, isVat=True).update(tableStatus='Available', isVat=False)
        RestaurantTable.objects.filter(tableNo=totable, isVat=False).update(tableStatus='Occupied',isVat=True)
    return redirect('restaurants:dines')
# END TRANSFER TABLE Section========================================================================

# Logout Section====================================================================================
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
# END Logout Section================================================================================
  

def sample_view(request):
    papersize = 76
    papersize1 = 38
    # msg = 'ryan viajedor'
    # for i in msg:
    #     print(i, end='')
    # print('')
    string2="Ryan M. Viajedor"
    # string_length=len(string2)+10    # will be adding 10 extra spaces
    # string_revised=string2.rjust(string_length)
    # print (string_revised)
    minusSTR1 = papersize1 - (len(string2)/2) + len(string2)
    print(minusSTR1)
    print(string2.rjust(int(minusSTR1), '0'))
    minusSTR = papersize -len(string2)
    print(minusSTR)
    divideSTR = minusSTR / 2
    print(divideSTR)
    print(string2.rjust(int(divideSTR), '0'))

    possettings = POSSetting.objects.all()
    for possetting in possettings:
        companyName = papersize1 - (len(possetting.companyName)/2) + len(possetting.companyName)
        print(possetting.companyName)
        print(companyName)
        print(possetting.companyName.rjust(int(companyName), '0'))

# DOWNLOAD Section================================================================================
@login_required(login_url="/accounts/login/")
def downloaddine_view(request, tableNo, refNo):
    dirname = 'C:/Users/RND-03/Documents/djangoprojects/posrestaurant/posrestaurant/web/static/Orders'
    if not os.path.exists(dirname):
        os.mkdir(os.path.join(dirname))

    tableno         = tableNo
    orderno         = refNo

    print(tableno)
    print(orderno)

    possettings = POSSetting.objects.all()
    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(referenceNo=orderno, isVat=True, isCancelled=False, isVoid=False)
    totalamount = TempRestaurantOrderDetail.objects.filter(referenceNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = TempRestaurantOrderDetail.objects.filter(referenceNo=orderno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('qtySold'))['sum']

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    if not tableno:
        tableno = 'TAKEOUT'

    today = timezone.now()
    user = request.user.username
    params = {
            'possettings':possettings,
            'orderno':orderno,
            'today': today,
            'tableno': tableno,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'user': user
        }
    # return render_to_pdf('bill.html', params)

    pdf = render_to_pdf('printorders.html', params)
    response =  HttpResponse(pdf, content_type='application/pdf')
    filename = "Order_%s.pdf" %(orderno)
    # filename = "Invoice.pdf"
    content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response
    
    # return redirect('restaurants:dines')

@login_required(login_url="/accounts/login/")
def printdine_view(request):
    dirname = 'C:/Users/RND-03/Documents/djangoprojects/posrestaurant/posrestaurant/web/static/Orders'
    if not os.path.exists(dirname):
        os.mkdir(os.path.join(dirname))

    tableno         = request.POST.get("tableNo") 
    # orderno         = request.POST.get("refNo") 

    print(tableno)
    # print(orderno)

    possettings = POSSetting.objects.all()
    getOrderDetailsLists = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True, isCancelled=False, isVoid=False)
    totalamount = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = TempRestaurantOrderDetail.objects.filter(tableNo=tableno, isVat=True, isCancelled=False, isVoid=False).aggregate(sum=Sum('qtySold'))['sum']

    for getOrderDetailsList in getOrderDetailsLists:
        orderno = getOrderDetailsList.referenceNo
    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    if not tableno:
        tableno = 'TAKEOUT'

    today = timezone.now()
    user = request.user.username
    params = {
            'possettings':possettings,
            'orderno':orderno,
            'today': today,
            'tableno': tableno,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'user': user
        }
    return render_to_pdf('printorders.html', params)

@login_required(login_url="/accounts/login/")
def printtakeout_view(request):

    tableno         = request.POST.get("tableNo") 
    orderno         = request.POST.get("refNo") 

    print(tableno)
    print(orderno)

    possettings = POSSetting.objects.all()
    getOrderDetailsLists = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=False, isCancelled=False, isVoid=False)
    totalamount = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=False, isCancelled=False, isVoid=False).aggregate(sum=Sum('totalAmount'))['sum']
    totalitems = RestaurantOrderDetail.objects.filter(orderNo=orderno, isVat=False, isCancelled=False, isVoid=False).aggregate(sum=Sum('qtySold'))['sum']

    if not totalamount:
        totalamount = 0
    totalVATsale = float(totalamount) / 1.12
    totalVAT = totalVATsale * 0.12

    if not tableno:
        tableno = 'TAKEOUT'

    today = timezone.now()
    user = request.user.username
    params = {
            'possettings':possettings,
            'orderno':orderno,
            'today': today,
            'tableno': tableno,
            'items': getOrderDetailsLists,
            'totalamount': totalamount,
            'totalitems': totalitems,
            'totalVATsale': totalVATsale,
            'totalVAT': totalVAT,
            'user': user
        }
    return render_to_pdf('printorders.html', params)
# END DOWNLOAD Section============================================================================