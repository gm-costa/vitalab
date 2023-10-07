from django.urls import path
from . import views


urlpatterns = [
    path('gerar-acesso/', views.gerar_acesso_medico, name="gerar_acesso_medico"),
    path('acesso-medico/<str:token>', views.acesso_medico, name="acesso_medico"),
]
