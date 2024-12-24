from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 
            'email', 
            'location', 
            'birth_date', 
            'bio', 
            'avatar',
            'password1',
            'password2'
            )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class CustomUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)