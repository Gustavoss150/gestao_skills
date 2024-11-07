from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse


def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    # Sua lógica de login padrão aqui
    return render(request, 'core/login.html')

def login_rh(request):
    # Lógica para login como RH (admin)
    return render(request, 'core/login_rh.html')

