from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from .models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
