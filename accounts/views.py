from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserLoginForm
from .utils import send_email   


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            # Send email
            email = form.cleaned_data.get('email')
            subject = 'Welcome to our site'
            message = 'Thank you for registering on our site'
            send_email(subject, email, message)

            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Error creating your account')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('/')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('/')
