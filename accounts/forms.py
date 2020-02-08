from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import MyUser
from django.contrib.auth import get_user_model

class UserLoginForm(forms.Form):
    # """Form to login user"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class UserRegistrationForm(UserCreationForm):
     # """Form to register user"""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)
         
    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password1', 'password2']
        

    def clean_email(self):
        User = get_user_model()
        email = self.cleaned_data.get('email') #1
        username = self.cleaned_data.get('username')
        #2 check if the email is unique, using the Django ORM
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique')
        return email
    
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError("Passwords must match")
            
        return password2
        
