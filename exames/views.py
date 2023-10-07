from datetime import date, datetime
# import os
# import sys
# from django.http import HttpResponse
# from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import TiposExames, SolicitacaoExame, PedidosExames


@login_required(login_url='/usuarios/login/')
def solicitar_exame(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == 'POST':
        exames_id = request.POST.getlist('exames')

        if len(exames_id) == 0:
            messages.add_message(request, messages.WARNING, 'Nenhum exame foi selecionado!')
            return render(request, 'solicitar_exame.html', {'tipos_exames': tipos_exames})

        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        # preco_total = solicitacao_exames.aggregate(total=Sum('preco'))['total']
        preco_total = 0
        for exame in solicitacao_exames:
            if exame.disponivel:
                preco_total += exame.preco

        context = {
            'solicitacao_exames': solicitacao_exames,
            'preco_total': preco_total,
            'tipos_exames': tipos_exames,
            'data_exame': date.today()
        }
        return render(request, 'solicitar_exame.html', context)

    else:
        return render(request, 'solicitar_exame.html', {'tipos_exames': tipos_exames})


@login_required(login_url='/usuarios/login/')
def fechar_pedido(request):
    if request.method == 'POST':
        exames_id = request.POST.getlist('exames-solicitados')
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

        pedido_exame = PedidosExames(
            usuario = request.user,
            data = datetime.now()
        )

        pedido_exame.save()

        for exame in solicitacao_exames:
            solicitacao_exames_temp = SolicitacaoExame(
                usuario=request.user,
                exame=exame,
                status="E"
            )
            solicitacao_exames_temp.save()
            pedido_exame.exames.add(solicitacao_exames_temp)
            
        pedido_exame.save()

        messages.add_message(request, messages.SUCCESS, 'Pedido de exame concluído com sucesso.')
        return redirect(reverse('gerenciar_pedidos'))


@login_required(login_url='/usuarios/login')
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})


@login_required(login_url='/usuarios/login')
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidosExames, pk=pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request, messages.ERROR, 'Esse pedido não lhe pertence')
        return redirect(reverse('gerenciar_pedidos'))

    pedido.agendado = False
    pedido.save()
    messages.add_message(request, messages.SUCCESS, 'Pedido cancelado com sucesso')
    return redirect(reverse('gerenciar_pedidos'))


@login_required(login_url='/usuarios/login')
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)

    return render(request, 'gerenciar_exames.html', {'exames': exames})


@login_required(login_url='/usuarios/login')
def permitir_abrir_exame(request, exame_id):
    exame = get_object_or_404(SolicitacaoExame, pk=exame_id)

    if not exame.usuario == request.user:
        messages.add_message(request, messages.ERROR, 'Esse exame não lhe pertence')
        return redirect(reverse('gerenciar_exames'))
    
    if not exame.requer_senha:
        # verificar se o pdf existe

        # if not os.path.join(settings.BASE_DIR, exame.resultado.url).exists():
        #     messages.add_message(request, messages.ERROR, 'Não existe PDF para o exame!')
        #     return redirect(reverse('gerenciar_exames'))
        # else:
        #     return redirect(exame.resultado.url)

        return redirect(exame.resultado.url)

    else: 
        return redirect(f'/exames/solicitar-senha-exame/{exame.id}')


@login_required(login_url='/usuarios/login')
def solicitar_senha_exame(request, exame_id):
    exame = get_object_or_404(SolicitacaoExame, pk=exame_id)
    if request.method == "GET":
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == "POST":
        senha = request.POST.get("senha")

        if len(senha) == 0:
            messages.add_message(request, messages.WARNING, 'Senha não informada!')
            return redirect(f'/exames/solicitar-senha-exame/{exame.id}')

        if not exame.usuario == request.user:
            messages.add_message(request, messages.ERROR, 'Esse exame não lhe pertence')
            return redirect(f'/exames/solicitar-senha-exame/{exame.id}')

        if not senha == exame.senha:
            messages.add_message(request, messages.ERROR, 'Senha inválida!')
            return redirect(f'/exames/solicitar-senha-exame/{exame.id}')

        return redirect(exame.resultado.url)
