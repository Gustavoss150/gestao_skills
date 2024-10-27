from django.db import models
from django.utils import timezone

class Skill(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    data_contratacao = models.DateField(default=timezone.now)
    skills = models.ManyToManyField('Skill', related_name='funcionarios')
    comprovacao_treinamento = models.BooleanField(default=False)  # Status de treinamento
    

    def __str__(self):
        return self.nome


