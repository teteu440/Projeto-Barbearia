from datetime import timedelta

from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nome = models.CharField('Nome completo', max_length=150)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail', blank=True, null=True)
    data_nascimento = models.DateField('Data de nascimento', blank=True, null=True)
    criado_em = models.DateTimeField('Cadastrado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Barbeiro(models.Model):
    nome = models.CharField('Nome completo', max_length=150)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail', blank=True, null=True)
    especialidade = models.CharField('Especialidade', max_length=100, blank=True)
    data_contratacao = models.DateField('Data de contratação', blank=True, null=True)
    criado_em = models.DateTimeField('Cadastrado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Barbeiro'
        verbose_name_plural = 'Barbeiros'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField('Nome do serviço', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    preco = models.DecimalField('Preço (R$)', max_digits=8, decimal_places=2)
    duracao_minutos = models.PositiveIntegerField('Duração (minutos)')
    criado_em = models.DateTimeField('Cadastrado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    class Status(models.TextChoices):
        AGENDADO = 'agendado', 'Agendado'
        CONFIRMADO = 'confirmado', 'Confirmado'
        CONCLUIDO = 'concluido', 'Concluído'
        CANCELADO = 'cancelado', 'Cancelado'
        FALTOU = 'faltou', 'Não compareceu'

    # Status que ocupam o horário do barbeiro/cliente (cancelados e faltas liberam).
    STATUS_OCUPAM = ('agendado', 'confirmado', 'concluido')

    cliente = models.ForeignKey(
        Cliente, verbose_name='Cliente', on_delete=models.PROTECT, related_name='agendamentos')
    barbeiro = models.ForeignKey(
        Barbeiro, verbose_name='Barbeiro', on_delete=models.PROTECT, related_name='agendamentos')
    servico = models.ForeignKey(
        Servico, verbose_name='Serviço', on_delete=models.PROTECT, related_name='agendamentos')
    inicio = models.DateTimeField('Início')
    fim = models.DateTimeField('Término', editable=False)
    preco = models.DecimalField(
        'Valor (R$)', max_digits=8, decimal_places=2, null=True, editable=False)
    status = models.CharField(
        'Status', max_length=12, choices=Status.choices, default=Status.AGENDADO)
    observacoes = models.TextField('Observações', blank=True)
    criado_em = models.DateTimeField('Cadastrado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['inicio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._servico_original = self.servico_id

    def __str__(self):
        quando = timezone.localtime(self.inicio).strftime('%d/%m/%Y %H:%M')
        return f'{self.cliente} — {self.servico} em {quando}'

    def save(self, *args, **kwargs):
        # O término vem da duração do serviço. O valor é "congelado" no momento
        # do agendamento, para que mudanças futuras no preço não alterem o histórico.
        self.fim = self.inicio + timedelta(minutes=self.servico.duracao_minutos)
        if self.preco is None or self.servico_id != self._servico_original:
            self.preco = self.servico.preco
        super().save(*args, **kwargs)
        self._servico_original = self.servico_id
