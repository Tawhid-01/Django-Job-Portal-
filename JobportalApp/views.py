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
    data = JobPostModel.objects.all()
    context = {
        'job_post':data
    }

    return render(req,'page/dashboard.html',context)

def viewJobPage(req,id):
    job = JobPostModel.objects.get(id=id)
    context = {
        'job':job,
        'title': job.title

    }
    return render(req,'page/view.html',context)

def editJobPage(req,id):
    job = JobPostModel.objects.get(id=id)
    if req.user.user_type == "Recruiter":

        if req.method =='POST':
            form = JobPostForm(req.POST,instance=job)
            if form.is_valid(): 
                data = form.save(commit=False)
                data.user = req.user
                data.save()
                return redirect('dashboard')

    form = JobPostForm(instance=job)
    context = {
        'form':form,
        'form_title':"Edit A New Job",
        'btn':"Edit",
    }
    return render(req,'base/base_form.html',context)

def deleteJobPage(req,id):
    JobPostModel.objects.get(id=id).delete()

    return redirect('dashboard')

def recruiterProfilePage(req):
    try:
       user= R_ProfileModel.objects.get(user=req.user)
    except R_ProfileModel.DoesNotExist:
        user =R_ProfileModel.objects.create(user=req.user)

    if req.method == 'POST':
        form = RecruiterForm(req.POST,req.FILES,instance=user)
        if form.is_valid():
            user =form.save(commit=False)
            user.user = req.user
            user.save()
            return redirect('dashboard')

    form = RecruiterForm(instance=user)
    context ={
        'form':form,
        'title':'Recruiter Form',
        'btn':'Submit',
        'user':user
    }

    return render(req,'base/base_form.html',context)


def seekerProfilePage(req):
    try:
       user= S_ProfileModel.objects.get(user=req.user)
    except S_ProfileModel.DoesNotExist:
        user =S_ProfileModel.objects.create(user=req.user)

    if req.method == 'POST':
        form = SeekerForm(req.POST,req.FILES,instance=user)
        if form.is_valid():
            user =form.save(commit=False)
            user.user = req.user
            user.save()
            return redirect('dashboard')

    form = SeekerForm(instance=user)
    context ={
        'form':form,
        'title':'Seeker Form',
        'btn':'Submit',
        'user':user
    }

    return render(req,'base/base_form.html',context)

def jobPostPage(req):
    if req.user.user_type == "Recruiter":

        if req.method =='POST':
            form = JobPostForm(req.POST)
            if form.is_valid(): 
                data = form.save(commit=False)
                data.user = req.user
                data.save()
                return redirect('dashboard')

    form = JobPostForm()
    context={
        'form':form,
        'title':'Job Post Form',
        'btn':'Submit'
    }
    return render(req,'base/base_form.html',context)