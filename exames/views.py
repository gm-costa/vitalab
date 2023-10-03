from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/usuario/login/')
def solicitar(request):
    return render(request, 'solicitar_exame.html')
