from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    USER_TYPE =[
        ('JobSeeker','JobSeeker'),
        ('Recruiter','Recruiter'),
    ]
    display_name = models.CharField(max_length=100,null=True,blank=True)

    user_type = models.CharField(max_length=20,choices=USER_TYPE,null=True,blank=True)

    def __str__(self):
        return self.username
    
class R_ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    position = models.CharField(max_length=100,null=True,blank=True)
    company = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    company_website = models.CharField(max_length=100,null=True,blank=True)
    profile = models.ImageField(upload_to='media/profile/',null=True,blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class S_ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE , related_name='seeker')
    name = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    skill = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(upload_to='media/resume/',null=True,blank=True)

    def __str__(self):
        return self.name
    
class JobPostModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    number_of_openings = models.CharField(max_length=100,null=True,blank=True)
    position = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    job_type = models.CharField(max_length=100,null=True,blank=True)
    salary = models.CharField(max_length=100,null=True,blank=True)
    job_description = models.TextField(null=True,blank=True)
    deadline = models.DateTimeField(auto_now_add=False)
    skill_set = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.title
    
class ApplyJobModel(models.Model):
    STATUS =[
        ('Pending','Pending'),
        ('Shortlisted','Shortlisted'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
    ]
    job_seeker = models.ForeignKey(S_ProfileModel, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPostModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,choices=STATUS,null=True,default='Pending')

    def __str__(self):
        return f"{self.job_seeker} - {self.status} - {self.job}" 