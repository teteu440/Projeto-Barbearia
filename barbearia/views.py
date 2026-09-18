from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import ClienteForm


def index(request):
    return HttpResponse('<h1>Sistema de Gerenciamento de Barbearia</h1>')


def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cadastro_cliente')
    else:
        form = ClienteForm()

    return render(request, 'barbearia/cadastro.html', {'form': form})