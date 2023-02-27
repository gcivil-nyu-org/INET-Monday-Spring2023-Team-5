from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Business


def index_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    return render(request, 'users/index.html', {
        'welcome': 'Welcome {}!'.format(request.user.first_name),
        'message': 'Welcome, {}'.format(request.user.first_name)
        }
)


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
        'message': 'LOGGED OUT!'
    })


def add_business_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == 'POST':
        business = Business(
            name=request.POST['name'],
            address=request.POST['address'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            owner=request.user,
        )
        business.save()
        
        return HttpResponseRedirect(reverse('view_business', args=(business.id,)))
    
    return render(request, 'users/add_business.html', {
        'message': 'Add your business.'
    })

def view_business_view(request, business_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    business = Business.objects.get(id=business_id)
    
    return render(request, 'users/view_business.html', {
        'message': 'View your business.',
        'business': business,
    })
