from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def cadastro(request):
    if request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:    
            messages.add_message(request, messages.ERROR, 'As senhas não coincidem!')
            return redirect(reverse('cadastro'))
        
        if len(senha) < 6:
            messages.add_message(request, messages.ERROR, 'A senha deve ter 6 (seis) carecteres ou mais!')
            return redirect(reverse('cadastro'))
        
        try:
            # Username deve ser único!
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
        except:
            messages.add_message(request, messages.ERROR, 'Não foi possível salvar os dados do cadastro!')
            return redirect(reverse('cadastro'))

        return redirect(reverse('cadastro'))
    else:
        return render(request, 'cadastro.html')


def logar(request):
    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
						# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Usuario ou senha inválidos')
            return redirect(reverse('login'))
    
    else:
        return render(request, 'login.html')