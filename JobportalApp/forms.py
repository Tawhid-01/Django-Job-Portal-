from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *

class UserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username','display_name','email','password1','password2','user_type']

class AuthForm(AuthenticationForm):
    class Meta:
        model = UserModel
        fields = ['username','password1']


class RecruiterForm(forms.ModelForm):
    class Meta:
        model = R_ProfileModel
        fields = '__all__'
        exclude = ['user']

class SeekerForm(forms.ModelForm):
    class Meta:
        model = S_ProfileModel
        fields = '__all__'
        exclude = ['user']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPostModel
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

# class ApplyJobForm(form.ModelForm):
#     class Meta:
#         model = ApplyJobModel
#         fields = '__all__'
#         exclude = ['job_seeker','status']