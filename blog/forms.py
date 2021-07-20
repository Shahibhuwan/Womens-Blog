from django.db.models import fields
from blog.models import Customer
from django.contrib.auth.models import User
from django import forms
from django.db import models

class UserRegistration(forms.ModelForm):
    username =forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model=Customer
        fields=['username','password','email','full_name','image','phone','profession' ,'currently_working']