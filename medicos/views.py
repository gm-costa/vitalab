from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from exames.models import PedidosExames
from .models import AcessoMedico


@login_required(login_url='/usuarios/login')
def gerar_acesso_medico(request):
    if request.method == "GET":
        acessos_medicos = AcessoMedico.objects.filter(usuario =request. user)
        return render(request, 'gerar_acesso_medico.html', {'acessos_medicos': acessos_medicos})
    elif request.method == "POST":
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get("data_exame_inicial")
        data_exame_final = request.POST.get("data_exame_final")

        acesso_medico = AcessoMedico(
            usuario = request.user,
            identificacao = identificacao,
            tempo_de_acesso = tempo_de_acesso,
            data_exames_iniciais = data_exame_inicial,
            data_exames_finais = data_exame_final
            # criado_em = datetime.now()
        )

        try:
            acesso_medico.save()
            messages.add_message(request, messages.SUCCESS, 'Acesso gerado com sucesso')
        except:
            messages.add_message(request, messages.ERROR, 'Não foi possível salvar os dados')

        return redirect(reverse('gerar_acesso_medico'))


# @login_required(login_url='/usuarios/login')
def acesso_medico(request, token):
    acesso_medico = get_object_or_404(AcessoMedico, token=token)
    # acesso_medico = AcessoMedico.objects.filter(token=token)

    if acesso_medico.status == 'Expirado':
        messages.add_message(request, messages.WARNING, f'O link "{acesso_medico.url}" está expirado!')
        return redirect(reverse('gerar_acesso_medico'))

    pedidos = PedidosExames.objects.filter(data__gte = acesso_medico.data_exames_iniciais).filter(data__lte = acesso_medico.data_exames_finais).filter(usuario=acesso_medico.usuario)

    return render(request, 'acesso_medico.html', {'pedidos': pedidos})
