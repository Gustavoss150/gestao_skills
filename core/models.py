from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Setor(models.Model):
    nome = models.CharField(max_length=100)
    gestor = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

class Cargo(models.Model):
    nome = models.CharField(max_length=100)  # Renomeado para ser consistente com o admin.py
    descricao = models.TextField(blank=True, null=True)  # Adicionado para compatibilidade com o admin.py
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Skill(models.Model):
    nome = models.CharField(max_length=100)  # Renomeado para ser consistente com o admin.py
    descricao = models.TextField(blank=True, null=True)  # Renomeado para ser consistente com o admin.py

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, through='FuncionarioSkill')
    is_rh = models.BooleanField(default=False)
    is_gestor = models.BooleanField(default=False)
    data_contratacao = models.DateField(default=now)
    comprovacao_treinamento = models.BooleanField(default=False)
    
    # Campo opcional para o usuário
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        # Verifica se o cargo é "Gestor" ou "RH" e atribui o campo usuario
        if self.cargo.nome in ["Gestor", "RH"]:
            if not self.usuario:  # Caso não tenha um usuário atribuído
                raise ValueError("Funcionário do RH ou Gestor deve ter um usuário atribuído.")
        else:
            # Se o cargo não for "Gestor" ou "RH", garantir que o campo 'usuario' seja nulo
            self.usuario = None

        super(Funcionario, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

class FuncionarioSkill(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)
