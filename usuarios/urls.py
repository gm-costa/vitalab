from django.urls import path
from .views import cadastro, logar, sair

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', logar, name='login'),
    path('sair/', sair, name='sair'),
]
