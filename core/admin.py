from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Funcionario

# Função para criar grupos e permissões
def create_groups():
    # Criando grupo de RH/Admin com todas as permissões
    rh_group, created = Group.objects.get_or_create(name='RH')
    if created:
        rh_permissions = Permission.objects.all()  # Dá todas as permissões
        rh_group.permissions.set(rh_permissions)

    # Criando grupo de Gestores com permissões específicas
    gestor_group, created = Group.objects.get_or_create(name='Gestor')
    if created:
        gestor_permissions = Permission.objects.filter(codename__in=[
            'add_funcionario', 'change_funcionario', 'view_funcionario'
        ])
        gestor_group.permissions.set(gestor_permissions)

    # Grupo de Funcionários, com permissão apenas de visualizar seus dados
    funcionario_group, created = Group.objects.get_or_create(name='Funcionario')
    if created:
        funcionario_permissions = Permission.objects.filter(codename__in=['view_funcionario'])
        funcionario_group.permissions.set(funcionario_permissions)

