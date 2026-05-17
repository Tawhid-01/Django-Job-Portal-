from django.urls import path
from .views import *

urlpatterns = [
    path('register/',registerPage,name='register'),
    path('',loginPage,name='login'),
    path('logout/',logoutPage,name='logout'),
    path('dashboard/',dashboardPage,name='dashboard'),

    path('recruiter/',recruiterProfilePage,name='recruiterProfile'),
    path('seeker/',seekerProfilePage,name='seekerProfile'),

    path('jobpost/',jobPostPage,name='jobpost'),
    path('jobdetail/<int:id>/',viewJobPage,name='jobdetail'),
    path('editjob/<int:id>/',editJobPage,name='editjob'),
    path('deletejob/<int:id>/',deleteJobPage,name='deletejob'),
    path('jobapply/<int:id>/',applyJobPage,name='applyJob'),

    path('view-apply/',viewApplicantPage,name='viewApplicant'),
    path('showApplicant/<int:id>/',showApplicant,name='showApplicant'),

    path('shortlist/<int:id>/',shortList,name='shortlist'),
    path('reject/<int:id>/',rejectPage,name='reject'),

    path('skill-match/',skillMatchPage,name='skillMatch'),
    path('skill-add/',skillAddPage,name='skillAdd'),
    
]
