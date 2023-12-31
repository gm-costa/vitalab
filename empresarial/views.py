from django.http import FileResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required
from empresarial.utils import gerar_pdf_exames, gerar_senha_aleatoria
from exames.models import SolicitacaoExame
from django.contrib import messages


@staff_member_required 
def gerenciar_clientes(request):
    clientes = User.objects.filter(is_staff=False)

    nome_completo = request.GET.get('nome')
    email = request.GET.get('email')

    if email:
        clientes = clientes.filter(email__contains = email)
    if nome_completo:
        clientes = clientes.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__contains=nome_completo)

    context = {'clientes': clientes, 'nome_completo': nome_completo, 'email': email}

    return render(request, 'gerenciar_clientes.html', context)


@staff_member_required 
def cliente(request, cliente_id):
    cliente = get_object_or_404(User, pk=cliente_id)
    exames = SolicitacaoExame.objects.filter(usuario=cliente)

    return render(request, 'cliente.html', {'cliente': cliente, 'exames': exames})


@staff_member_required 
def exame_cliente(request, exame_id):
    exame = get_object_or_404(SolicitacaoExame, id=exame_id)
    # print('resultado:', exame.resultado)
    return render(request, 'exame_cliente.html', {'exame': exame})


@staff_member_required 
def proxy_pdf(request, exame_id):
    exame = get_object_or_404(SolicitacaoExame, id=exame_id)

    #TODO: verificar existencia do pdf

    response = exame.resultado.open()
    return FileResponse(response)


@staff_member_required 
def gerar_senha(request, exame_id):
    exame = get_object_or_404(SolicitacaoExame, id=exame_id)

    if exame.senha:
        # Baixar o documento da senha já existente
        return FileResponse(gerar_pdf_exames(exame.exame.nome, exame.usuario, exame.senha), filename="token.pdf")
    
    senha = gerar_senha_aleatoria(9)
    exame.senha = senha
    exame.save()
    return FileResponse(gerar_pdf_exames(exame.exame.nome, exame.usuario, exame.senha), filename="token.pdf")


@staff_member_required 
def alterar_dados_exame(request, exame_id):
    exame = get_object_or_404(SolicitacaoExame, id=exame_id)

    pdf = request.FILES.get('resultado')
    status = request.POST.get('status')
    requer_senha = request.POST.get('requer_senha')
    
    if requer_senha and (not exame.senha):
        messages.add_message(request, messages.ERROR, 'Para exigir a senha primeiro crie uma.')
        return redirect(f'/empresarial/exame-cliente/{exame_id}')
    
    exame.requer_senha = True if requer_senha else False

    if pdf:
        exame.resultado = pdf
        
    exame.status = status
    exame.save()
    messages.add_message(request, messages.SUCCESS, 'Alteração realizada com sucesso')
    return redirect(f'/empresarial/exame-cliente/{exame_id}')
