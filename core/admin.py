from django.contrib import admin
from .models import Funcionario, Skill
from django.contrib.auth.models import User, Group

admin.site.unregister(User)

admin.site.unregister(Group)

# Personalizando o título do site admin
admin.site.site_header = "Skills Enforce"
admin.site.site_title = "Gestão de Skills Admin"
admin.site.index_title = "Bem-vindo à Gestão de Skills"

# Alterando o texto "Site administration"
admin.site.index_template = "admin/index.html"
admin.site.site_title = "Skills Enforce"
admin.site.site_header = "Skills Enforce"


# Configuração do admin para as Skills
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

# Configuração do admin para Funcionários
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'data_contratacao', 'comprovacao_treinamento')
    search_fields = ('nome', 'cargo')
    list_filter = ('cargo', 'comprovacao_treinamento')
    
    # Habilitando a edição de skills no mesmo formulário
    filter_horizontal = ('skills',)

    # Personalizando o formulário de adição/edição de funcionários
    fieldsets = (
        (None, {
            'fields': ('nome', 'cargo', 'data_contratacao')
        }),
        ('Skills e Treinamento', {
            'fields': ('skills', 'comprovacao_treinamento')
        }),
    )


