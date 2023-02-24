from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    return render(request, 'users/index.html', {
        'message': 'Hello, {} {}! You are logged in.'.format(request.user.first_name, request.user.last_name)
    })


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)


        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'users/login.html', {
                'message': 'Invalid credentials.'
            })
        
    return render(request, 'users/login.html', {
        'message': 'Please log in.'
    })


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'users/register.html', {
                'message': 'Passwords must match.'
            })
        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {
                'message': 'Email already exists.'
            })
        
        user = User.objects.create_user(
            email=email,
            password=password1,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            username=email,
        )
        user = authenticate(request, username=email, password=password1)

        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'users/register.html', {
        'message': 'Please register.'
    })


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    logout(request)

    return render(request, 'users/logout.html', {
        'message': 'You have been logged out.'
    })
