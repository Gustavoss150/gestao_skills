from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

# Modelo de Setor
class Setor(models.Model):
    nome = models.CharField(max_length=100)
    gestor = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


# Modelo de Cargo
class Cargo(models.Model):
    nome = models.CharField(max_length=100)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    competencias = models.TextField(blank=True, null=True)
    escopo_atividade = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


# Modelo de Skill
class Skill(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


# Modelo de Funcionario
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
        # Verifica se o cargo é "Gestor" ou "RH" e garante a associação com um usuário
        if self.cargo.nome in ["Gestor", "RH"] and not self.usuario:
            raise ValueError("Funcionário do RH ou Gestor deve ter um usuário atribuído.")
        # Se não for RH nem Gestor, garante que o campo 'usuario' seja nulo
        if self.cargo.nome not in ["Gestor", "RH"]:
            self.usuario = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


# Modelo de FuncionarioSkill com campo de nível
class FuncionarioSkill(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)
    nivel = models.PositiveIntegerField(default=1)  # Nível da skill (1 a 4)

    class Meta:
        unique_together = ('funcionario', 'skill')  # Evita duplicação de relação

    def __str__(self):
        return f"{self.funcionario.nome} - {self.skill.nome} (Nível {self.nivel})"


# Modelo de Notificação
class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['usuario', 'lida']),
            models.Index(fields=['data_criacao']),
        ]

    def __str__(self):
        return f"Notificação para {self.usuario.username} - {'Lida' if self.lida else 'Não lida'}"


# Signal para criar notificação ao adicionar um novo funcionário
@receiver(post_save, sender=Funcionario)
def criar_notificacao_novo_funcionario(sender, instance, created, **kwargs):
    if created and instance.setor:
        mensagem = f"Novo funcionário '{instance.nome}' adicionado ao setor '{instance.setor.nome}'."
        
        # Envia a notificação para todos os gestores do setor
        gestores_do_setor = User.objects.filter(funcionario__setor=instance.setor, funcionario__is_gestor=True)
        
        for gestor in gestores_do_setor:
            Notificacao.objects.create(usuario=gestor, mensagem=mensagem)


class Treinamento(models.Model):
    nome = models.CharField(max_length=200)  # Campo atual para nome do treinamento
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)
    funcionarios = models.ManyToManyField(Funcionario)

    def __str__(self):
        # Retorna o nome dos funcionários relacionados e a data de início
        funcionarios_nomes = ", ".join(funcionario.nome for funcionario in self.funcionarios.all())
        return f"Treinamento de {funcionarios_nomes} - {self.data_inicio.strftime('%d/%m/%Y') if self.data_inicio else 'Sem data'}"        
