from django.urls import path
from . import views


urlpatterns = [
    path('solicitar/', views.solicitar_exame, name='solicitar_exame'),
    path('fechar-pedido/', views.fechar_pedido, name='fechar_pedido'),
    path('gerenciar-pedidos/', views.gerenciar_pedidos, name="gerenciar_pedidos"),
    path("cancelar-pedido/<int:pedido_id>", views.cancelar_pedido, name="cancelar_pedido"),
    path('gerenciar-exames/', views.gerenciar_exames, name="gerenciar_exames"),
    path('permitir-abrir-exame/<int:exame_id>', views.permitir_abrir_exame, name="permitir_abrir_exame"),
    path('solicitar-senha-exame/<int:exame_id>', views.solicitar_senha_exame, name="solicitar_senha_exame"),
]
