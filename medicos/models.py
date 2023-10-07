from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from secrets import token_urlsafe
from django.shortcuts import redirect
from django.urls import reverse


class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField(auto_now_add=True)
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20, blank=True, null=True)

    @property
    def status(self):
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'
    
    @property
    def url(self):
        # return redirect(reverse('acesso_medico', kwargs={'token': self.token}))
        return f"http://127.0.0.1:8000/medicos/acesso-medico/{self.token}"

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Acessos Medicos'
