

# Create your views here.


from django.shortcuts import render, redirect

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    # Sua lógica de login padrão aqui
    return render(request, 'core/login.html')

def login_rh(request):
    # Lógica para login como RH
    return render(request, 'core/login_rh.html')

def login_gestor(request):
    # Lógica para login como Gestor
    return render(request, 'core/login_gestor.html')

