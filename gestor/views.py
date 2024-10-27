from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse
from .models import Funcionario


def dashboard_gestor(request):
    # Dados de exemplo para exibição no template
    funcionarios = [
        {
            'nome': 'Funcionario 1',
            'cargo': 'Analista',
            'data_contratacao': '2023-01-01',
            'skills': [{'nome': 'Python', 'descricao': 'Linguagem de programação'}],
            'treinamento': 'Sim'
        },
        # Outros funcionários...
    ]
    return render(request, 'base_gestor.html', {'funcionarios': funcionarios})

def login_gestor(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff:  # Verifica se o usuário não é um admin
                login(request, user)
                return redirect('dashboard_gestor')  # Redireciona para a página do gestor após login
            else:
                messages.error(request, 'Você não tem permissão para acessar como gestor.')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'core/login_gestor.html', {'form': form})


def dashboard_gestor(request):
    funcionarios = Funcionario.objects.prefetch_related('skills').all()
    return render(request, 'base_gestor.html', {'funcionarios': funcionarios})