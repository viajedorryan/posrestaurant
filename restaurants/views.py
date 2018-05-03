from django.shortcuts import render, redirect
from django.contrib.auth import logout
from core.models import *
import datetime

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


def dine_view(request):
    categories = ProductCategory.objects.all()
    # beverage = ProductCategory.objects.get(description='Beverages')
    # appetizer = ProductCategory.objects.get(description='Appetizer')
    # salad = ProductCategory.objects.get(description='Salad')
    # main = ProductCategory.objects.get(description='MainDish')
    products = Product.objects.all()

    
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


        # print(code)
        # print(code)
        # print(name)
        # print(user)
        # print(salessummary)
    # for category in categories:
    #     if category.description == 'Beverages':
    #         beverages = Product.objects.filter(productCategoryID=1)
    #         # print(beverages)

    #     if category.description == 'Appetizer':
    #         appetizers = Product.objects.filter(productCategoryID=2)

    #     if category.description == 'Salad':
    #         salads = Product.objects.filter(productCategoryID=3)

    #     if category.description == 'MainDish':
    #         maindishes = Product.objects.filter(productCategoryID=4)

    # print(beverages)
    # print(appetizers)
    # print(salads)
    # print(maindishes)

    template='dine.html'
    context = {'categories': categories, 'beverages': beverages}
    return render(request, template, context)


def takeout_view(request):
    template='takeout.html'
    context = {}
    return render(request, template, context)


def delivery_view(request):
    template='delivery.html'
    context = {}
    return render(request, template, context)
    
def beverage_view(request):
    beverages = Product.objects.filter(productCategoryID=1)
    template='beverages/beverages.html'
    context = {'beverages': beverages}
    return render(request, template, context)
    
def appetizer_view(request):
    appetizers = Product.objects.filter(productCategoryID=2)
    template='appetizers/appetizers.html'
    context = {'appetizers': appetizers}
    return render(request, template, context)

def salad_view(request):
    salads = Product.objects.filter(productCategoryID=3)
    template='salads/salads.html'
    context = {'salads': salads}
    return render(request, template, context)

def main_view(request):
    maindishes = Product.objects.filter(productCategoryID=4)
    template='maindishes/maindish.html'
    context = {'maindishes': maindishes}
    return render(request, template, context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')