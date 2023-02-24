from django.shortcuts import render


def index_view(request):
    return render(request, 'users/index.html')

def login_view(request):
    return render(request, 'users/login.html')

def register_view(request):
    return render(request, 'users/register.html')

def logout_view(request):
    return render(request, 'users/logout.html')
