from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def cadastro(request):
    if request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if User.objects.filter(username=username):
            messages.add_message(request, messages.ERROR, 'Username já existente!')
            return render(request, 'cadastro.html', request.POST.dict())

        if not senha == confirmar_senha:    
            messages.add_message(request, messages.ERROR, 'As senhas não coincidem!')
            return render(request, 'cadastro.html', request.POST.dict())
        
        if len(senha) < 6:
            messages.add_message(request, messages.ERROR, 'A senha deve ter 6 (seis) carecteres ou mais!')
            return render(request, 'cadastro.html', request.POST.dict())
        
        try:
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
            messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso.')
            return redirect(reverse('cadastro'))
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, e) #'Não foi possível salvar os dados do cadastro!')
            return render(request, 'cadastro.html', request.POST.dict())
    else:
        if request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, 'Você já está logado.')
            return redirect(reverse('solicitar_exame'))
        
        return render(request, 'cadastro.html')


def logar(request):
    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
            return redirect(reverse('solicitar_exame'))
        else:
            messages.add_message(request, messages.ERROR, 'Usuario ou senha inválidos')
            return redirect(reverse('login'))
    
    else:
        if request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, 'Você já está logado.')
            return redirect(reverse('solicitar_exame'))
        
        return render(request, 'login.html')
    

def sair(request):
    logout(request)
    return redirect(reverse('login'))
