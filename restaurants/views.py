from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
# function based view
def home_view(request):
    template='home.html'
    context = {}
    return render(request, template, context)


def dine_view(request):
    template='dine.html'
    context = {}
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