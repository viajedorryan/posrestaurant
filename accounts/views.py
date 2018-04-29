from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
# function based view
def signup_view(request):
    template='signup.html'
    # form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('accounts:signup')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, template, context)

def login_view(request):
    template='login.html'
    # form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in the user
            user = form.get_user()
            login(request, user)
            return redirect('accounts:signup')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, template, context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')