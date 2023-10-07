from django.contrib import admin
from .models import AcessoMedico


class AcessoMedicoAdmin(admin.ModelAdmin):
    list_display = ('identificacao', 'tempo_de_acesso', 'criado_em', 'token', 'status')

admin.site.register(AcessoMedico, AcessoMedicoAdmin)

