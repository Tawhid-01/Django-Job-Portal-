from django.shortcuts import render,redirect
from .models import *
from.forms import *
from django.contrib.auth import login,logout
from django.contrib import messages


# Create your views here.

def registerPage(req):

    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    form = UserForm()
    context={
        'form':form,
        'title':'Registration',
        'btn':'Register'
    }
    return render(req,'account/base_account_form.html',context)

def loginPage(req):

    if req.method == 'POST':
        form = AuthForm(req,req.POST)
        if form.is_valid():
            user =form.get_user()
            login(req,user)
            return redirect('dashboard')

    form = AuthForm()
    context={
        'form':form,
        'title':'Login Form',
        'btn':'Login'
    }
    return render(req,'account/base_account_form.html',context)

def logoutPage(req):
    logout(req)
    return redirect('login')

def dashboardPage(req):

    return render(req,'page/dashboard.html')