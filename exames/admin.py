from django.contrib import admin
from .models import TiposExames, PedidosExames, SolicitacaoExame


class SolicitacaoExameAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'exame', 'status', 'resultado')


admin.site.register(TiposExames)
admin.site.register(PedidosExames)
admin.site.register(SolicitacaoExame, SolicitacaoExameAdmin)
