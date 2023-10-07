from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class TiposExames(models.Model):
    tipo_choices = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de Sangue')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Tipos Exames'
    
class SolicitacaoExame(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'

    def badge_template(self):
        if self.status == 'E':
            classes_css = 'bg-fundo text-dark px-4 py-2'
            texto = "Em análise"
        elif self.status == 'F':
            classes_css = 'bg-success px-4 py-2'
            texto = "Finalizado"
        
        return mark_safe(f"<span class='badge {classes_css}'>{texto}</span>")

class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario} | {self.data}'

    class Meta:
        verbose_name_plural = 'Pedidos Exames'