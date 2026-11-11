from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import Cliente, Barbeiro, Servico

# Aceita (84) 99999-0000, (84) 9999-0000, 84999990000, etc.
validar_telefone = RegexValidator(
    r'^\(?\d{2}\)?\s?9?\d{4}-?\d{4}$',
    'Informe um telefone válido, ex.: (84) 99999-0000.',
)


class ClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefone'].validators.append(validar_telefone)

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if Cliente.objects.filter(telefone=telefone).exists():
            raise ValidationError('Já existe um cliente com este telefone.')
        return telefone

    def clean_data_nascimento(self):
        data = self.cleaned_data.get('data_nascimento')
        if data and data > date.today():
            raise ValidationError('A data de nascimento não pode ser futura.')
        return data

    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com',
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


class BarbeiroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefone'].validators.append(validar_telefone)

    class Meta:
        model = Barbeiro
        fields = ['nome', 'telefone', 'email', 'especialidade', 'data_contratacao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com',
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Corte, Barba, Coloração',
            }),
            'data_contratacao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


class ServicoForm(forms.ModelForm):
    def clean_preco(self):
        preco = self.cleaned_data['preco']
        if preco <= 0:
            raise ValidationError('O preço deve ser maior que zero.')
        return preco

    def clean_duracao_minutos(self):
        duracao = self.cleaned_data['duracao_minutos']
        if duracao < 1:
            raise ValidationError('A duração deve ser de pelo menos 1 minuto.')
        return duracao

    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'duracao_minutos']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Corte de cabelo',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva o serviço (opcional)',
                'rows': 3,
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
            }),
            'duracao_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 30',
            }),
        }