from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    # Sua lógica de login padrão aqui
    return render(request, 'core/login.html')

def login_rh(request):
    # Lógica para login como RH
    return render(request, 'core/login_rh.html')

def login_gestor(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff:  # Verifica se o usuário não é um admin
                login(request, user)
                return redirect('core/login_gestor.html')  # Redireciona para a página do gestor após login
            else:
                messages.error(request, 'Você não tem permissão para acessar como gestor.')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'core/login_gestor.html', {'form': form})

def dashboard_gestor(request):
    return render(request, 'core/dashboard_gestor.html')  # Certifique-se de que o template existe
