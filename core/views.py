from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .models import Funcionario

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    # Sua lógica de login padrão aqui
    return render(request, 'core/login.html')

def login_rh(request):
    # Lógica para login como RH (admin)
    return render(request, 'core/login_rh.html')

def exportar_funcionarios(request):
    """
    View para exportar funcionários em um arquivo CSV.
    """
    # Configura o tipo de resposta como CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.csv"'

    # Cria o writer para escrever o conteúdo do CSV
    writer = csv.writer(response)

    # Cabeçalhos do CSV
    writer.writerow(['Nome', 'Setor', 'Cargo', 'Data de Contratação', 'Treinamento Concluído', 'Skills'])

    # Dados dos funcionários
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


