from django.contrib import admin

from .models import Agendamento, Barbeiro, Cliente, Servico

admin.site.site_header = 'Barbearia — Administração'
admin.site.site_title = 'Barbearia'
admin.site.index_title = 'Painel administrativo'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'criado_em')
    search_fields = ('nome', 'telefone', 'email')
    date_hierarchy = 'criado_em'


@admin.register(Barbeiro)
class BarbeiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'especialidade', 'criado_em')
    search_fields = ('nome', 'telefone', 'especialidade')
    list_filter = ('especialidade',)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao_minutos', 'criado_em')
    search_fields = ('nome',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('inicio', 'cliente', 'barbeiro', 'servico', 'status', 'preco')
    list_filter = ('status', 'barbeiro')
    list_select_related = ('cliente', 'barbeiro', 'servico')
    date_hierarchy = 'inicio'
    autocomplete_fields = ('cliente',)
    readonly_fields = ('fim', 'preco')
