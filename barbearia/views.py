from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import ClienteForm, BarbeiroForm, ServicoForm
from .models import Cliente, Barbeiro, Servico


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
    return render(request, 'barbearia/cadastro.html', {'form': form, 'titulo': 'Cadastro de Cliente'})


def cadastro_barbeiro(request):
    if request.method == 'POST':
        form = BarbeiroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barbeiro cadastrado com sucesso!')
            return redirect('cadastro_barbeiro')
    else:
        form = BarbeiroForm()
    return render(request, 'barbearia/cadastro.html', {'form': form, 'titulo': 'Cadastro de Barbeiro'})


def cadastro_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return redirect('cadastro_servico')
    else:
        form = ServicoForm()
    return render(request, 'barbearia/cadastro.html', {'form': form, 'titulo': 'Cadastro de Serviço'})


def listar_clientes(request):
    clientes = Cliente.objects.all()
    colunas = ['Nome', 'Telefone', 'E-mail', 'Data de nascimento']
    linhas = [
        [c.nome, c.telefone, c.email or '-', c.data_nascimento or '-']
        for c in clientes
    ]
    return render(request, 'barbearia/listagem.html', {
        'titulo': 'Clientes cadastrados',
        'aba_ativa': 'clientes',
        'colunas': colunas,
        'linhas': linhas,
    })


def listar_barbeiros(request):
    barbeiros = Barbeiro.objects.all()
    colunas = ['Nome', 'Telefone', 'Especialidade', 'Data de contratação']
    linhas = [
        [b.nome, b.telefone, b.especialidade or '-', b.data_contratacao or '-']
        for b in barbeiros
    ]
    return render(request, 'barbearia/listagem.html', {
        'titulo': 'Barbeiros cadastrados',
        'aba_ativa': 'barbeiros',
        'colunas': colunas,
        'linhas': linhas,
    })


def listar_servicos(request):
    servicos = Servico.objects.all()
    colunas = ['Nome', 'Preço (R$)', 'Duração (min)']
    linhas = [
        [s.nome, f'{s.preco:.2f}', s.duracao_minutos]
        for s in servicos
    ]
    return render(request, 'barbearia/listagem.html', {
        'titulo': 'Serviços cadastrados',
        'aba_ativa': 'servicos',
        'colunas': colunas,
        'linhas': linhas,
    })