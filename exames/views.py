from django.shortcuts import render
from django.http import HttpResponse


def solicitar(request):
    return HttpResponse('Solcitar exame')
