from django.shortcuts import render
from django.http import JsonResponse

def lista_clientes(request):
    return JsonResponse({'message': 'Lista de clientes', 'clientes': []})