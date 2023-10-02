from django.urls import path
from .views import cadastro, logar

urlpatterns = [
    path('cadastro', cadastro, name='cadastro'),
    path('login', logar, name='login'),
]
