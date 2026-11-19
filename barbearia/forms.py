import re
from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Agendamento, Barbeiro, Cliente, Servico


def formatar_telefone(valor):
    """Valida um telefone brasileiro (DDD + 8 ou 9 dígitos) e devolve formatado."""
    digitos = re.sub(r'\D', '', valor or '')
    if len(digitos) not in (10, 11):
        raise forms.ValidationError('Informe um telefone válido com DDD, ex: (11) 91234-5678.')
    if len(digitos) == 11:
        return f'({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}'
    return f'({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}'


def campo_data(**attrs):
    # O formato ISO é necessário para o <input type="date"> exibir a data ao editar.
    return forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', **attrs})


class BootstrapLikeFormMixin:
    """Aplica a classe CSS 'form-control' a todos os campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs.setdefault('class', 'form-control')


class ClienteForm(BootstrapLikeFormMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome completo'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'}),
            'data_nascimento': campo_data(),
        }

    def clean_telefone(self):
        return formatar_telefone(self.cleaned_data['telefone'])


class BarbeiroForm(BootstrapLikeFormMixin, forms.ModelForm):
    class Meta:
        model = Barbeiro
        fields = ['nome', 'telefone', 'email', 'especialidade', 'data_contratacao']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome completo'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'}),
            'especialidade': forms.TextInput(attrs={'placeholder': 'Ex: Degradê, barba'}),
            'data_contratacao': campo_data(),
        }

    def clean_telefone(self):
        return formatar_telefone(self.cleaned_data['telefone'])


class ServicoForm(BootstrapLikeFormMixin, forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'duracao_minutos']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Corte de cabelo'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descreva o serviço (opcional)', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'min': '0.01'}),
            'duracao_minutos': forms.NumberInput(attrs={'placeholder': 'Ex: 30', 'min': '1'}),
        }

    def clean_preco(self):
        preco = self.cleaned_data['preco']
        if preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero.')
        return preco

    def clean_duracao_minutos(self):
        duracao = self.cleaned_data['duracao_minutos']
        if duracao <= 0:
            raise forms.ValidationError('A duração deve ser de pelo menos 1 minuto.')
        return duracao


class AgendamentoForm(BootstrapLikeFormMixin, forms.ModelForm):
    inicio = forms.DateTimeField(
        label='Data e hora',
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Agendamento
        fields = ['cliente', 'barbeiro', 'servico', 'inicio', 'status', 'observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Opcional'}),
        }

    def clean(self):
        dados = super().clean()
        inicio, servico = dados.get('inicio'), dados.get('servico')
        if not inicio or not servico:
            return dados

        if self.instance.pk is None and inicio < timezone.now():
            self.add_error('inicio', 'Não é possível agendar em um horário que já passou.')
            return dados

        if dados.get('status') in Agendamento.STATUS_OCUPAM:
            fim = inicio + timedelta(minutes=servico.duracao_minutos)
            conflitantes = Agendamento.objects.filter(
                status__in=Agendamento.STATUS_OCUPAM, inicio__lt=fim, fim__gt=inicio,
            ).exclude(pk=self.instance.pk).select_related('cliente', 'barbeiro')

            for campo, rotulo in (('barbeiro', 'O barbeiro'), ('cliente', 'O cliente')):
                escolhido = dados.get(campo)
                outro = escolhido and conflitantes.filter(**{campo: escolhido}).first()
                if outro:
                    de = timezone.localtime(outro.inicio).strftime('%H:%M')
                    ate = timezone.localtime(outro.fim).strftime('%H:%M')
                    self.add_error(campo, f'{rotulo} já tem um agendamento das {de} às {ate} nesse período.')
        return dados
