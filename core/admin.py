from django.contrib import admin
from .models import Funcionario, Skill, Setor, Cargo, FuncionarioSkill
from django.contrib.auth.models import User, Group
import csv  # Import necessário para exportar CSV
from django.http import HttpResponse  # Import necessário para resposta HTTP

# Remover User e Group do admin, como antes
admin.site.unregister(User)
admin.site.unregister(Group)

# Personalizar o título do site admin
admin.site.site_header = "Skills Enforce"
admin.site.site_title = "Gestão de Skills Admin"
admin.site.index_title = "Bem-vindo à Gestão de Skills"
admin.site.index_template = "admin/index.html"

# Função para exportar funcionários em CSV
def exportar_funcionarios_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.csv"'
    writer = csv.writer(response)

    # Cabeçalhos do CSV
    writer.writerow(['Nome', 'Setor', 'Cargo', 'Data de Contratação', 'Treinamento Concluído', 'Skills'])

    # Dados dos funcionários selecionados
    for funcionario in queryset.select_related('setor', 'cargo').prefetch_related('skills'):
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

# Descrição da ação para exibição no admin
exportar_funcionarios_csv.short_description = "Exportar selecionados para CSV"

# Configuração do admin para as Skills
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

# Configuração do admin para Cargos
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'setor')
    search_fields = ('nome',)
    list_filter = ('setor',)

# Inline para exibir funcionários dentro dos setores
class FuncionarioInline(admin.TabularInline):
    model = Funcionario
    extra = 0

# Configuração do admin para Setores
@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_funcionarios', 'get_cargos')
    search_fields = ('nome',)
    inlines = [FuncionarioInline]

    def get_funcionarios(self, obj):
        return ", ".join([funcionario.nome for funcionario in obj.funcionario_set.all()])
    get_funcionarios.short_description = 'Funcionários'

    def get_cargos(self, obj):
        return ", ".join(set(funcionario.cargo.nome for funcionario in obj.funcionario_set.all() if funcionario.cargo))
    get_cargos.short_description = 'Cargos'

# Inline para FuncionarioSkill
class FuncionarioSkillInline(admin.TabularInline):
    model = FuncionarioSkill
    extra = 1  # Quantidade de linhas extras para adicionar habilidades

# Configuração do admin para Funcionários com permissões de RH e gestor
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'data_contratacao', 'comprovacao_treinamento')
    search_fields = ('nome', 'cargo__nome')
    list_filter = ('cargo', 'comprovacao_treinamento')

    # Adicionar a Inline para gerenciar skills através de FuncionarioSkill
    inlines = [FuncionarioSkillInline]

    # Adicionando a ação de exportação
    actions = [exportar_funcionarios_csv]

    # Personalizando o formulário de adição/edição de funcionários
    fieldsets = (
        (None, {
            'fields': ('nome', 'setor', 'cargo', 'data_contratacao', 'comprovacao_treinamento')
        }),
    )

    # Restringir a visualização de funcionários por setor para gestores
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.funcionario.is_rh:
            return qs  # RH vê todos os funcionários
        elif request.user.funcionario.is_gestor:
            return qs.filter(setor=request.user.funcionario.setor)  # Gestor vê apenas seu setor
        return qs.none()  # Caso de usuários sem permissão definida

    # Permitir adição apenas para RH
    def has_add_permission(self, request):
        return request.user.funcionario.is_rh

    # Permitir alterações com base no cargo e setor
    def has_change_permission(self, request, obj=None):
        if request.user.funcionario.is_rh:
            return True  # RH pode modificar qualquer um
        if request.user.funcionario.is_gestor:
            return obj and obj.setor == request.user.funcionario.setor  # Gestor pode modificar apenas seu setor
        return False

    # Permitir exclusão apenas para RH
    def has_delete_permission(self, request, obj=None):
        return request.user.funcionario.is_rh

