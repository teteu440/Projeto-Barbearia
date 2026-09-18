from django.db import models


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