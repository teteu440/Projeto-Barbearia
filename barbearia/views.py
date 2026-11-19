from datetime import date, datetime, time, timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import AgendamentoForm, BarbeiroForm, ClienteForm, ServicoForm
from .models import Agendamento, Barbeiro, Cliente, Servico
from .notificacoes import enviar_email, link_whatsapp, montar_mensagem

VAZIO = '—'


def valor_ou_vazio(valor):
    return VAZIO if valor in (None, '') else valor


class HomeView(LoginRequiredMixin, TemplateView):
    """Painel inicial com totais e últimos clientes cadastrados."""

    template_name = 'barbearia/home.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto.update(
            nav_ativa='home',
            total_clientes=Cliente.objects.count(),
            total_barbeiros=Barbeiro.objects.count(),
            total_servicos=Servico.objects.count(),
            ultimos_clientes=Cliente.objects.order_by('-criado_em')[:5],
            total_hoje=Agendamento.objects.filter(
                inicio__date=timezone.localdate(),
                status__in=Agendamento.STATUS_OCUPAM,
            ).count(),
            proximos=Agendamento.objects.filter(
                inicio__gte=timezone.now(),
                status__in=('agendado', 'confirmado'),
            ).select_related('cliente', 'barbeiro', 'servico')[:5],
        )
        return contexto


class EntidadeMixin(LoginRequiredMixin):
    """Configuração compartilhada pelas telas de cada entidade.

    Cada entidade define: model, form_class, prefixo (usado nos nomes das
    URLs), nome no singular/plural e a chave de navegação.
    """

    model = None
    form_class = None
    prefixo = ''
    nome = ''
    nome_plural = ''

    def get_success_url(self):
        return reverse_lazy(f'{self.prefixo}_list')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto.update(
            nav_ativa=self.nome_plural.lower(),
            nome=self.nome,
            nome_plural=self.nome_plural,
            lista_url=reverse(f'{self.prefixo}_list'),
        )
        return contexto


class EntidadeListView(EntidadeMixin, ListView):
    template_name = 'barbearia/list.html'
    paginate_by = 10
    campos_busca = ()
    colunas = ()  # lista de (rótulo, função que recebe o objeto)

    def get_queryset(self):
        queryset = super().get_queryset()
        termo = self.request.GET.get('q', '').strip()
        if termo and self.campos_busca:
            filtro = Q()
            for campo in self.campos_busca:
                filtro |= Q(**{f'{campo}__icontains': termo})
            queryset = queryset.filter(filtro)
        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['colunas'] = [rotulo for rotulo, _ in self.colunas]
        contexto['linhas'] = [
            {
                'valores': [valor_ou_vazio(extrair(obj)) for _, extrair in self.colunas],
                'editar_url': reverse(f'{self.prefixo}_update', args=[obj.pk]),
                'excluir_url': reverse(f'{self.prefixo}_delete', args=[obj.pk]),
            }
            for obj in contexto['object_list']
        ]
        contexto['criar_url'] = reverse(f'{self.prefixo}_create')
        contexto['termo_busca'] = self.request.GET.get('q', '').strip()
        return contexto


class EntidadeCreateView(EntidadeMixin, SuccessMessageMixin, CreateView):
    template_name = 'barbearia/form.html'

    def get_success_message(self, cleaned_data):
        return f'{self.nome} cadastrado com sucesso!'


class EntidadeUpdateView(EntidadeMixin, SuccessMessageMixin, UpdateView):
    template_name = 'barbearia/form.html'

    def get_success_message(self, cleaned_data):
        return f'{self.nome} atualizado com sucesso!'


class EntidadeDeleteView(EntidadeMixin, DeleteView):
    template_name = 'barbearia/confirm_delete.html'

    def form_valid(self, form):
        resposta = super().form_valid(form)
        messages.success(self.request, f'{self.nome} excluído com sucesso!')
        return resposta


# --- Clientes ---------------------------------------------------------------

class ClienteMixin(EntidadeMixin):
    model = Cliente
    form_class = ClienteForm
    prefixo = 'cliente'
    nome = 'Cliente'
    nome_plural = 'Clientes'


class ClienteListView(ClienteMixin, EntidadeListView):
    campos_busca = ('nome', 'telefone', 'email')
    colunas = (
        ('Nome', lambda c: c.nome),
        ('Telefone', lambda c: c.telefone),
        ('E-mail', lambda c: c.email),
        ('Nascimento', lambda c: c.data_nascimento and c.data_nascimento.strftime('%d/%m/%Y')),
    )


class ClienteCreateView(ClienteMixin, EntidadeCreateView):
    pass


class ClienteUpdateView(ClienteMixin, EntidadeUpdateView):
    pass


class ClienteDeleteView(ClienteMixin, EntidadeDeleteView):
    pass


# --- Barbeiros --------------------------------------------------------------

class BarbeiroMixin(EntidadeMixin):
    model = Barbeiro
    form_class = BarbeiroForm
    prefixo = 'barbeiro'
    nome = 'Barbeiro'
    nome_plural = 'Barbeiros'


class BarbeiroListView(BarbeiroMixin, EntidadeListView):
    campos_busca = ('nome', 'telefone', 'especialidade')
    colunas = (
        ('Nome', lambda b: b.nome),
        ('Telefone', lambda b: b.telefone),
        ('Especialidade', lambda b: b.especialidade),
        ('Contratação', lambda b: b.data_contratacao and b.data_contratacao.strftime('%d/%m/%Y')),
    )


class BarbeiroCreateView(BarbeiroMixin, EntidadeCreateView):
    pass


class BarbeiroUpdateView(BarbeiroMixin, EntidadeUpdateView):
    pass


class BarbeiroDeleteView(BarbeiroMixin, EntidadeDeleteView):
    pass


# --- Serviços ---------------------------------------------------------------

class ServicoMixin(EntidadeMixin):
    model = Servico
    form_class = ServicoForm
    prefixo = 'servico'
    nome = 'Serviço'
    nome_plural = 'Serviços'


class ServicoListView(ServicoMixin, EntidadeListView):
    campos_busca = ('nome', 'descricao')
    colunas = (
        ('Nome', lambda s: s.nome),
        ('Preço', lambda s: f'R$ {s.preco:.2f}'.replace('.', ',')),
        ('Duração', lambda s: f'{s.duracao_minutos} min'),
    )


class ServicoCreateView(ServicoMixin, EntidadeCreateView):
    pass


class ServicoUpdateView(ServicoMixin, EntidadeUpdateView):
    pass


class ServicoDeleteView(ServicoMixin, EntidadeDeleteView):
    pass


# --- Agenda -----------------------------------------------------------------

def _parse_data(valor):
    try:
        return date.fromisoformat(valor)
    except (TypeError, ValueError):
        return None


def _parse_id(valor):
    return int(valor) if valor and valor.isdigit() else None


class AgendaView(LoginRequiredMixin, TemplateView):
    """Agenda do dia, com navegação entre dias e filtro por barbeiro."""

    template_name = 'barbearia/agenda.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        hoje = timezone.localdate()
        dia = _parse_data(self.request.GET.get('data')) or hoje
        barbeiro_id = _parse_id(self.request.GET.get('barbeiro'))

        inicio_dia = timezone.make_aware(datetime.combine(dia, time.min))
        agendamentos = Agendamento.objects.filter(
            inicio__gte=inicio_dia, inicio__lt=inicio_dia + timedelta(days=1),
        ).select_related('cliente', 'barbeiro', 'servico')
        if barbeiro_id:
            agendamentos = agendamentos.filter(barbeiro_id=barbeiro_id)

        def link(d):
            parametros = {'data': d.isoformat()}
            if barbeiro_id:
                parametros['barbeiro'] = barbeiro_id
            return '?' + urlencode(parametros)

        faturamento = agendamentos.filter(
            status=Agendamento.Status.CONCLUIDO).aggregate(total=Sum('preco'))['total'] or 0
        contexto.update(
            nav_ativa='agendamentos',
            dia=dia,
            eh_hoje=dia == hoje,
            agendamentos=agendamentos,
            barbeiros=Barbeiro.objects.all(),
            barbeiro_id=barbeiro_id,
            link_anterior=link(dia - timedelta(days=1)),
            link_proximo=link(dia + timedelta(days=1)),
            link_hoje=link(hoje),
            total_ocupados=agendamentos.filter(status__in=Agendamento.STATUS_OCUPAM).count(),
            faturamento=f'{faturamento:.2f}'.replace('.', ','),
            novo_url=reverse('agendamento_create') + link(dia),
        )
        return contexto


class AgendamentoMixin(EntidadeMixin):
    model = Agendamento
    form_class = AgendamentoForm
    prefixo = 'agendamento'
    nome = 'Agendamento'
    nome_plural = 'Agendamentos'

    def get_success_url(self):
        # Volta para a agenda do dia do agendamento.
        dia = timezone.localtime(self.object.inicio).date().isoformat() if self.object.pk else ''
        return reverse('agendamento_list') + (f'?data={dia}' if dia else '')


class AgendamentoCreateView(AgendamentoMixin, EntidadeCreateView):
    def get_success_url(self):
        # Depois de agendar, mostra a mensagem pronta para enviar ao cliente.
        return reverse('agendamento_comunicar', args=[self.object.pk])

    def form_valid(self, form):
        resposta = super().form_valid(form)
        cliente = self.object.cliente
        if settings.AGENDAMENTO_EMAIL_AUTOMATICO and cliente.email:
            if enviar_email(self.object):
                messages.success(self.request, f'E-mail de confirmação enviado para {cliente.email}.')
            else:
                messages.error(
                    self.request,
                    'Não foi possível enviar o e-mail de confirmação. Use a tela abaixo para tentar de novo.')
        return resposta

    def get_initial(self):
        inicial = super().get_initial()
        dia = _parse_data(self.request.GET.get('data'))
        if dia:
            inicial['inicio'] = datetime.combine(dia, time(9, 0))
        barbeiro_id = _parse_id(self.request.GET.get('barbeiro'))
        if barbeiro_id:
            inicial['barbeiro'] = barbeiro_id
        return inicial


class AgendamentoUpdateView(AgendamentoMixin, EntidadeUpdateView):
    pass


class AgendamentoDeleteView(AgendamentoMixin, EntidadeDeleteView):
    def get_success_url(self):
        return reverse('agendamento_list')


class AgendamentoStatusView(LoginRequiredMixin, View):
    """Muda o status de um agendamento (confirmar, concluir, cancelar, faltou)."""

    permitidos = ('confirmado', 'concluido', 'cancelado', 'faltou')
    http_method_names = ['post']

    def post(self, request, pk, status):
        if status not in self.permitidos:
            raise Http404('Status inválido.')
        agendamento = get_object_or_404(Agendamento, pk=pk)
        agendamento.status = status
        agendamento.save()
        messages.success(request, f'Agendamento marcado como “{agendamento.get_status_display()}”.')

        destino = request.POST.get('next', '')
        if not url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
            dia = timezone.localtime(agendamento.inicio).date().isoformat()
            destino = f"{reverse('agendamento_list')}?data={dia}"
        return redirect(destino)


class AgendamentoComunicarView(LoginRequiredMixin, TemplateView):
    """Mostra a mensagem do agendamento e permite enviá-la por WhatsApp ou e-mail."""

    template_name = 'barbearia/comunicar.html'

    def get_agendamento(self):
        return get_object_or_404(
            Agendamento.objects.select_related('cliente', 'barbeiro', 'servico'),
            pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        agendamento = self.get_agendamento()
        dia = timezone.localtime(agendamento.inicio).date().isoformat()
        contexto.update(
            nav_ativa='agendamentos',
            agendamento=agendamento,
            mensagem=montar_mensagem(agendamento),
            whatsapp_url=link_whatsapp(agendamento),
            agenda_url=f"{reverse('agendamento_list')}?data={dia}",
        )
        return contexto

    def post(self, request, *args, **kwargs):
        agendamento = self.get_agendamento()
        email = agendamento.cliente.email
        if not email:
            messages.error(request, 'Este cliente não tem e-mail cadastrado.')
        elif enviar_email(agendamento):
            messages.success(request, f'E-mail enviado para {email}.')
        else:
            messages.error(request, 'Não foi possível enviar o e-mail. Verifique a configuração de e-mail.')
        return redirect('agendamento_comunicar', pk=agendamento.pk)
