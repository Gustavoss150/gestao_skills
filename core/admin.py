from django import forms
from django.contrib import admin
from .models import Funcionario, Skill, Setor, Cargo, FuncionarioSkill, Treinamento
from django.contrib.auth.models import User, Group
import csv
from django.http import HttpResponse

# Remover User e Group do admin
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

    def get_model_perms(self, request):
        """Permitir que apenas o RH veja o modelo de Skill no admin."""
        perms = super().get_model_perms(request)
        try:
            if not request.user.funcionario.is_rh:
                perms['change'] = False
                perms['delete'] = False
                perms['add'] = False
        except Funcionario.DoesNotExist:
            perms['change'] = False
            perms['delete'] = False
            perms['add'] = False
        return perms

    # Não exibe o modelo de Skill para o Gestor no menu
    def get_list_display(self, request):
        if hasattr(request.user, 'funcionario') and request.user.funcionario.is_rh:
            return ('nome', 'descricao')  # Só exibe para RH
        return ()  # Para gestores, não exibe nada


# Configuração do admin para Cargos
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'setor', 'competencias', 'escopo_atividade')
    search_fields = ('nome',)
    list_filter = ('setor',)
    # Permite edição dos campos de competências e escopo de atividade
    fields = ('nome', 'setor', 'competencias', 'escopo_atividade')

    def get_model_perms(self, request):
        """Permitir que apenas o RH veja o modelo de Cargo no admin."""
        perms = super().get_model_perms(request)
        try:
            if not request.user.funcionario.is_rh:
                perms['change'] = False
                perms['delete'] = False
                perms['add'] = False
        except Funcionario.DoesNotExist:
            perms['change'] = False
            perms['delete'] = False
            perms['add'] = False
        return perms

    def get_list_display(self, request):
        if hasattr(request.user, 'funcionario') and request.user.funcionario.is_rh:
            return ('nome', 'setor', 'competencias', 'escopo_atividade')  # Exibe para RH
        return ()  # Para gestores, não exibe nada

    def get_search_results(self, request, queryset, search_term):
        """Filtrar a busca para que busque também nas competências e escopo de atividade"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset = queryset.filter(
                Q(competencias__icontains=search_term) | Q(escopo_atividade__icontains=search_term)
            )
        return queryset, use_distinct


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

    def get_model_perms(self, request):
        """Permitir que apenas o RH veja o modelo de Setor no admin."""
        perms = super().get_model_perms(request)
        try:
            if not request.user.funcionario.is_rh:
                perms['change'] = False
                perms['delete'] = False
                perms['add'] = False
        except Funcionario.DoesNotExist:
            perms['change'] = False
            perms['delete'] = False
            perms['add'] = False
        return perms

    def get_list_display(self, request):
        if hasattr(request.user, 'funcionario') and request.user.funcionario.is_rh:
            return ('nome', 'get_funcionarios', 'get_cargos')  # Só exibe para RH
        return ()  # Para gestores, não exibe nada


# Inline para FuncionarioSkill com campo de nível
class FuncionarioSkillInline(admin.TabularInline):
    model = FuncionarioSkill
    extra = 1
    fields = ('skill', 'nivel', 'data_adicao')
    readonly_fields = ('data_adicao',)
    

# Configuração do admin para Treinamentos
@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_funcionarios', 'skills_treinadas', 'data_inicio', 'data_fim', 'finalizado')
    search_fields = ('funcionarios__nome', 'skills__nome')
    list_filter = ('finalizado', 'data_inicio')
    filter_horizontal = ('skills', 'funcionarios')  # Para facilitar seleção no ManyToMany

    def nome_funcionarios(self, obj):
        """
        Retorna os nomes dos funcionários associados ao treinamento.
        """
        return ", ".join([funcionario.nome for funcionario in obj.funcionarios.all()])
    nome_funcionarios.short_description = 'Funcionários'

    def skills_treinadas(self, obj):
        """
        Retorna as skills associadas ao treinamento com o nível atual de cada funcionário.
        """
        skills_info = []
        for funcionario in obj.funcionarios.all():
            for relacao in funcionario.funcionarioskill_set.all():
                if relacao.skill in obj.skills.all():  # Filtrar apenas skills relacionadas ao treinamento
                    skills_info.append(f"{relacao.skill.nome} (Nível Atual: {relacao.nivel}, Próximo: {relacao.nivel + 1})")
        return "; ".join(skills_info)
    skills_treinadas.short_description = 'Skills e Níveis'

    def get_queryset(self, request):
        """
        Otimiza o queryset para evitar consultas excessivas.
        """
        qs = super().get_queryset(request)
        return qs.prefetch_related('funcionarios__funcionarioskill_set__skill')

# Configuração do admin para Funcionários com permissões de RH e gestor
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'setor', 'data_contratacao', 'comprovacao_treinamento', 'get_skills', )
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

    # Adicionar um método para exibir as habilidades na lista de funcionários
    def get_skills(self, obj):
        return ", ".join([skill.nome for skill in obj.skills.all()])
    get_skills.short_description = 'Skills'

    # Restringir a visualização de funcionários por setor para gestores
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # Superuser vê tudo
            return qs
        try:
            funcionario = request.user.funcionario
            if funcionario.is_rh:
                return qs  # RH vê todos os funcionários
            elif funcionario.is_gestor:
                return qs.filter(setor=funcionario.setor)  # Gestor vê apenas seu setor
        except Funcionario.DoesNotExist:
            return qs.none()  # Caso de usuários sem permissão definida
        return qs.none()

    # Permitir adição apenas para RH
    def has_add_permission(self, request):
        try:
            return request.user.funcionario.is_rh
        except Funcionario.DoesNotExist:
            return False

    # Permitir alterações com base no cargo e setor
    def has_change_permission(self, request, obj=None):
        try:
            funcionario = request.user.funcionario
            if funcionario.is_rh:
                return True  # RH pode modificar qualquer um
            if funcionario.is_gestor:
                return obj and obj.setor == funcionario.setor  # Gestor pode modificar apenas seu setor
        except Funcionario.DoesNotExist:
            return False
        return False

    # Permitir exclusão apenas para RH
    def has_delete_permission(self, request, obj=None):
        try:
            return request.user.funcionario.is_rh
        except Funcionario.DoesNotExist:
            return False

