from django.contrib import admin
from .models import Cliente, Barbeiro, Servico


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'criado_em')
    search_fields = ('nome', 'telefone', 'email')


@admin.register(Barbeiro)
class BarbeiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'especialidade', 'criado_em')
    search_fields = ('nome', 'telefone', 'especialidade')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao_minutos', 'criado_em')
    search_fields = ('nome',)