from django.shortcuts import render, redirect
from django.contrib.auth import logout
from core.models import *

# Create your views here.
# function based view
def home_view(request):
    template='home.html'
    context = {}
    return render(request, template, context)


def dine_view(request):
    categories = ProductCategory.objects.all()
    # beverage = ProductCategory.objects.get(description='Beverages')
    # appetizer = ProductCategory.objects.get(description='Appetizer')
    # salad = ProductCategory.objects.get(description='Salad')
    # main = ProductCategory.objects.get(description='MainDish')
    products = Product.objects.all()

    print(categories)
    for category in categories:
        if category.description == 'Beverages':
            beverages = Product.objects.filter(productCategoryID=1)
            # print(beverages)

        if category.description == 'Appetizer':
            appetizers = Product.objects.filter(productCategoryID=2)

        if category.description == 'Salad':
            salads = Product.objects.filter(productCategoryID=3)

        if category.description == 'MainDish':
            maindishes = Product.objects.filter(productCategoryID=4)

    # prod = []
    # for category in categories:
    #     prodcts = Product.obects.get(productCategoryID=category.id)
    #     print(prodcts)
    #     product = {
    #         'category_description': category.description,
    #         'product_description': products.description
    #     }

    #     prod.append(product)


    print(beverages)
    print(appetizers)
    print(salads)
    print(maindishes)


    template='dine.html'
    context = {'categories': categories, 'beverages': beverages, 'appetizers': appetizers, 'salads': salads, 'maindishes': maindishes}
    return render(request, template, context)


def takeout_view(request):
    template='takeout.html'
    context = {}
    return render(request, template, context)


def delivery_view(request):
    template='delivery.html'
    context = {}
    return render(request, template, context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')