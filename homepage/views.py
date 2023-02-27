from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index_view(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage/index.html')
    
    return render(request, 'homepage/index.html', {
        'welcome': 'Welcome {}!'.format(request.user.first_name)
    }
)