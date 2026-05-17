from django.shortcuts import render,redirect
from .models import *
from.forms import *
from django.contrib.auth import login,logout
from django.contrib import messages
from django.db.models import Q


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
    search = req.GET.get('query')
    if search:
        data = JobPostModel.objects.filter(
            Q(title__icontains=search)|
            Q(job_description__icontains=search)|
            Q(position__icontains=search)
        )
    else:
        data = JobPostModel.objects.all()
    context = {
        'job_post':data
    }

    return render(req,'page/dashboard.html',context)

def skillMatchPage(req):
    try:
         user = S_ProfileModel.objects.get(user=req.user)
    except S_ProfileModel.DoesNotExist:
        return redirect('seekerProfile')
    
    if user:
        user_skill = user.skill.all()

        jobs = JobPostModel.objects.filter(skill_set__in=user_skill).distinct()
    context = {
        'jobs': jobs
    }
    return render(req,'page/skill_dashboard.html',context)

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

def skillAddPage(req):
    if req.method == 'POST':
        form = SkillForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form = SkillForm()
    context={
        'form':form,
        'title':'Add Skill',
        'btn':'Submit'
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
                form.save_m2m() # ManyToManyField 
                return redirect('dashboard')

    form = JobPostForm()
    context={
        'form':form,
        'title':'Job Post Form',
        'btn':'Submit'
    }
    return render(req,'base/base_form.html',context)


def applyJobPage(req,id):
    user = S_ProfileModel.objects.get(user=req.user)
    job = JobPostModel.objects.get(id=id)

    ApplyJobModel.objects.create(
        job_seeker = user,
        job = job,
        status = 'Pending'

        )
    messages.success(req,'Applied Successfully')
    return redirect('dashboard')

  
    

def viewApplicantPage(req):
    data = ApplyJobModel.objects.filter(job_seeker=req.user.seeker)
    context = {
        'jobs':data
    }
    return render(req,'page/myApplications.html',context)


def showApplicant(req,id):
    job_id = JobPostModel.objects.get(id=id)
    applicant = ApplyJobModel.objects.filter(job=job_id)

    context = {
        'applicants':applicant,
    }
    return render(req,'page/showApplicant.html',context)

def shortList(req,id):
    applicant = ApplyJobModel.objects.get(id=id)
    applicant.status = 'Shortlisted'
    applicant.save()
    return redirect('viewApplicant')

def rejectPage(req,id):
    apply = ApplyJobModel.objects.get(id=id)
    apply.status = "Rejected"
    apply.save()
    return redirect('viewApplicant')