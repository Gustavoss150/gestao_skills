from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Funcionario
import csv



def index(request):
    """
    Página inicial com opções de login para RH e Gestor.
    """
    return render(request, 'core/index.html')


def login_rh(request):
    """
    Login para usuários do tipo RH.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'funcionario') and user.funcionario.is_rh:
                login(request, user)
                return redirect('admin:index')  # Redireciona para o admin do Django
            else:
                return render(
                    request, 
                    'core/login_rh.html', 
                    {'form': form, 'error': 'Usuário não autorizado como RH.'}
                )
    else:
        form = AuthenticationForm()
    return render(request, 'core/login_rh.html', {'form': form})


def login_gestor(request):
    """
    Login para usuários do tipo Gestor.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'funcionario') and user.funcionario.is_gestor:
                login(request, user)
                return redirect('gestor_dashboard')  # Redireciona para o dashboard do gestor
            else:
                return render(
                    request, 
                    'core/login_gestor.html', 
                    {'form': form, 'error': 'Usuário não autorizado como Gestor.'}
                )
    else:
        form = AuthenticationForm()
    return render(request, 'core/login_gestor.html', {'form': form})


@login_required
def gestor_dashboard(request):
    """
    Dashboard para gestores, exibindo apenas funcionários do setor do gestor.
    """
    if not hasattr(request.user, 'funcionario') or not request.user.funcionario.is_gestor:
        return HttpResponse("Acesso não autorizado", status=403)

    setor_do_gestor = request.user.funcionario.setor
    funcionarios = Funcionario.objects.filter(setor=setor_do_gestor)

    return render(request, 'core/gestor_dashboard.html', {
        'funcionarios': funcionarios,
        'setor': setor_do_gestor
    })


@login_required
def exportar_funcionarios(request):
    """
    Exporta funcionários em um arquivo CSV.
    """
    if not request.user.is_staff:
        return HttpResponse("Acesso negado", status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Setor', 'Cargo', 'Data de Contratação', 'Treinamento Concluído', 'Skills'])

    funcionarios = Funcionario.objects.select_related('setor', 'cargo').prefetch_related('skills')
    for funcionario in funcionarios:
        skills = ", ".join(skill.nome for skill in funcionario.skills.all())
        writer.writerow([
            funcionario.nome,
            funcionario.setor.nome if funcionario.setor else "Sem Setor",
            funcionario.cargo.nome if funcionario.cargo else "Sem Cargo",
            funcionario.data_contratacao,
            "Sim" if funcionario.comprovacao_treinamento else "Não",
            skills
        ])

    return response
