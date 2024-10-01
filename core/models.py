from django.db import models

class GrupoSkill(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    # Outras fields
    grupos_skills = models.ManyToManyField(GrupoSkill, through='FuncionarioGrupoSkill')

class FuncionarioGrupoSkill(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)  # Chave para Funcionario
    grupo_skill = models.ForeignKey(GrupoSkill, on_delete=models.CASCADE)    # Chave para GrupoSkill
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('funcionario', 'grupo_skill')  # Evita duplicidade

