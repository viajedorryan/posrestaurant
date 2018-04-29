from django.shortcuts import render
from . import views

# Create your views here.
# function based view
def home(request):
    template='dashboard.html'
    context = {}
    return render(request, template, context)

# def properties(request):
#     template='properties.html'
#     context = {}
#     return render(request, template, context)

# def property_detail(request):
#     template='property_detail.html'
#     context = {}
#     return render(request, template, context)

# def search(request):
#     template='search.html'
#     context = {}
#     return render(request, template, context)

# def contact(request):
#     template='contact.html'
#     context = {}
#     return render(request, template, context)

# def about(request):
#     template='about.html'
#     context = {}
#     return render(request, template, context)
