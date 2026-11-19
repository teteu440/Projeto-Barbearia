from datetime import timedelta
from decimal import Decimal

from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .forms import ClienteForm, ServicoForm
from .models import Agendamento, Barbeiro, Cliente, Servico
from .notificacoes import link_whatsapp, montar_mensagem


class AutenticacaoTests(TestCase):
    def test_paginas_exigem_login(self):
        for nome in ('home', 'cliente_list', 'barbeiro_list', 'servico_list',
                     'cliente_create', 'barbeiro_create', 'servico_create',
                     'agendamento_list', 'agendamento_create'):
            with self.subTest(url=nome):
                resposta = self.client.get(reverse(nome))
                self.assertEqual(resposta.status_code, 302)
                self.assertIn(reverse('login'), resposta.url)

    def test_pagina_de_login_e_publica(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user('admin', password='senha-forte-123')

    def setUp(self):
        self.client.force_login(self.usuario)


class FormularioTests(TestCase):
    def dados_cliente(self, **extra):
        return {'nome': 'João Silva', 'telefone': '11912345678', **extra}

    def test_telefone_e_formatado(self):
        form = ClienteForm(self.dados_cliente())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['telefone'], '(11) 91234-5678')

    def test_telefone_fixo_com_10_digitos(self):
        form = ClienteForm(self.dados_cliente(telefone='(11) 3234-5678'))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['telefone'], '(11) 3234-5678')

    def test_telefone_invalido(self):
        form = ClienteForm(self.dados_cliente(telefone='123'))
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)

    def test_servico_rejeita_preco_e_duracao_invalidos(self):
        form = ServicoForm({'nome': 'Corte', 'preco': '0', 'duracao_minutos': '0'})
        self.assertFalse(form.is_valid())
        self.assertIn('preco', form.errors)
        self.assertIn('duracao_minutos', form.errors)


class ClienteCrudTests(BaseTestCase):
    def test_criar_cliente(self):
        resposta = self.client.post(reverse('cliente_create'), {
            'nome': 'Maria Souza', 'telefone': '11987654321',
            'email': 'maria@example.com', 'data_nascimento': '1990-05-20',
        })
        self.assertRedirects(resposta, reverse('cliente_list'))
        cliente = Cliente.objects.get()
        self.assertEqual(cliente.nome, 'Maria Souza')
        self.assertEqual(cliente.telefone, '(11) 98765-4321')

    def test_criar_cliente_invalido_mostra_erros(self):
        resposta = self.client.post(reverse('cliente_create'), {'nome': '', 'telefone': 'abc'})
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Cliente.objects.exists())

    def test_editar_cliente(self):
        cliente = Cliente.objects.create(nome='Ana', telefone='(11) 91111-2222')
        resposta = self.client.post(reverse('cliente_update', args=[cliente.pk]), {
            'nome': 'Ana Paula', 'telefone': '11911112222',
        })
        self.assertRedirects(resposta, reverse('cliente_list'))
        cliente.refresh_from_db()
        self.assertEqual(cliente.nome, 'Ana Paula')

    def test_formulario_de_edicao_mostra_data_preenchida(self):
        cliente = Cliente.objects.create(
            nome='Ana', telefone='(11) 91111-2222', data_nascimento='1991-02-03')
        resposta = self.client.get(reverse('cliente_update', args=[cliente.pk]))
        self.assertContains(resposta, 'value="1991-02-03"')

    def test_excluir_cliente(self):
        cliente = Cliente.objects.create(nome='Ana', telefone='(11) 91111-2222')
        self.assertEqual(self.client.get(reverse('cliente_delete', args=[cliente.pk])).status_code, 200)
        resposta = self.client.post(reverse('cliente_delete', args=[cliente.pk]))
        self.assertRedirects(resposta, reverse('cliente_list'))
        self.assertFalse(Cliente.objects.exists())

    def test_busca_filtra_resultados(self):
        Cliente.objects.create(nome='Carlos Lima', telefone='(11) 91111-1111')
        Cliente.objects.create(nome='Beatriz Rocha', telefone='(11) 92222-2222')
        resposta = self.client.get(reverse('cliente_list'), {'q': 'carlos'})
        self.assertContains(resposta, 'Carlos Lima')
        self.assertNotContains(resposta, 'Beatriz Rocha')

    def test_paginacao(self):
        for i in range(12):
            Cliente.objects.create(nome=f'Cliente {i:02d}', telefone='(11) 91111-1111')
        pagina1 = self.client.get(reverse('cliente_list'))
        self.assertEqual(len(pagina1.context['linhas']), 10)
        pagina2 = self.client.get(reverse('cliente_list'), {'page': 2})
        self.assertEqual(len(pagina2.context['linhas']), 2)


class BarbeiroEServicoTests(BaseTestCase):
    def test_criar_barbeiro(self):
        resposta = self.client.post(reverse('barbeiro_create'), {
            'nome': 'Pedro', 'telefone': '11933334444', 'especialidade': 'Barba',
        })
        self.assertRedirects(resposta, reverse('barbeiro_list'))
        self.assertEqual(Barbeiro.objects.get().especialidade, 'Barba')

    def test_criar_e_listar_servico(self):
        resposta = self.client.post(reverse('servico_create'), {
            'nome': 'Corte', 'preco': '45.50', 'duracao_minutos': '30',
        })
        self.assertRedirects(resposta, reverse('servico_list'))
        self.assertEqual(Servico.objects.get().preco, Decimal('45.50'))
        lista = self.client.get(reverse('servico_list'))
        self.assertContains(lista, 'R$ 45,50')
        self.assertContains(lista, '30 min')


class HomeTests(BaseTestCase):
    def test_painel_mostra_totais(self):
        Cliente.objects.create(nome='Ana', telefone='(11) 91111-2222')
        resposta = self.client.get(reverse('home'))
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['total_clientes'], 1)


def amanha(hora=10, minuto=0):
    """Amanhã no horário local indicado (sempre no futuro)."""
    return (timezone.localtime() + timedelta(days=1)).replace(
        hour=hora, minute=minuto, second=0, microsecond=0)


def texto(dt):
    return timezone.localtime(dt).strftime('%Y-%m-%dT%H:%M')


class AgendaBase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cliente = Cliente.objects.create(nome='Ana', telefone='(11) 91111-2222')
        self.outro_cliente = Cliente.objects.create(nome='Bia', telefone='(11) 93333-4444')
        self.barbeiro = Barbeiro.objects.create(nome='Pedro', telefone='(11) 95555-6666')
        self.outro_barbeiro = Barbeiro.objects.create(nome='Lucas', telefone='(11) 97777-8888')
        self.servico = Servico.objects.create(nome='Corte', preco=Decimal('40.00'), duracao_minutos=30)

    def criar(self, inicio=None, **extra):
        dados = dict(cliente=self.cliente, barbeiro=self.barbeiro, servico=self.servico,
                     inicio=inicio or amanha())
        dados.update(extra)
        return Agendamento.objects.create(**dados)

    def dados_post(self, inicio=None, **extra):
        dados = {
            'cliente': self.cliente.pk, 'barbeiro': self.barbeiro.pk, 'servico': self.servico.pk,
            'inicio': texto(inicio or amanha()), 'status': 'agendado', 'observacoes': '',
        }
        dados.update(extra)
        return dados


class AgendamentoModeloTests(AgendaBase):
    def test_fim_e_preco_sao_calculados(self):
        ag = self.criar(amanha(10, 0))
        self.assertEqual(ag.fim - ag.inicio, timedelta(minutes=30))
        self.assertEqual(ag.preco, Decimal('40.00'))

    def test_preco_historico_nao_muda_com_novo_preco_do_servico(self):
        ag = self.criar()
        self.servico.preco = Decimal('99.00')
        self.servico.save()
        ag.refresh_from_db()
        ag.observacoes = 'editado'
        ag.save()
        self.assertEqual(ag.preco, Decimal('40.00'))

    def test_trocar_servico_atualiza_preco_e_fim(self):
        ag = self.criar()
        barba = Servico.objects.create(nome='Barba', preco=Decimal('25.00'), duracao_minutos=20)
        ag.servico = barba
        ag.save()
        self.assertEqual(ag.preco, Decimal('25.00'))
        self.assertEqual(ag.fim - ag.inicio, timedelta(minutes=20))

    def test_servico_com_agendamento_nao_pode_ser_excluido(self):
        from django.db.models import ProtectedError
        self.criar()
        with self.assertRaises(ProtectedError):
            self.servico.delete()


class AgendamentoCrudTests(AgendaBase):
    def test_criar_agendamento(self):
        inicio = amanha(11, 0)
        resposta = self.client.post(reverse('agendamento_create'), self.dados_post(inicio))
        ag = Agendamento.objects.get()
        self.assertRedirects(resposta, reverse('agendamento_comunicar', args=[ag.pk]))
        self.assertEqual(timezone.localtime(ag.inicio).hour, 11)

    def test_nao_agenda_no_passado(self):
        passado = timezone.localtime() - timedelta(days=1)
        resposta = self.client.post(reverse('agendamento_create'), self.dados_post(passado))
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Agendamento.objects.exists())

    def test_conflito_de_horario_do_barbeiro(self):
        self.criar(amanha(10, 0))
        resposta = self.client.post(
            reverse('agendamento_create'),
            self.dados_post(amanha(10, 15), cliente=self.outro_cliente.pk))
        self.assertEqual(resposta.status_code, 200)
        self.assertIn('barbeiro', resposta.context['form'].errors)
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_conflito_de_horario_do_cliente(self):
        self.criar(amanha(10, 0))
        resposta = self.client.post(
            reverse('agendamento_create'),
            self.dados_post(amanha(10, 15), barbeiro=self.outro_barbeiro.pk))
        self.assertIn('cliente', resposta.context['form'].errors)

    def test_horarios_consecutivos_sao_permitidos(self):
        self.criar(amanha(10, 0))  # termina às 10:30
        self.client.post(reverse('agendamento_create'), self.dados_post(amanha(10, 30)))
        self.assertEqual(Agendamento.objects.count(), 2)

    def test_agendamento_cancelado_libera_horario(self):
        self.criar(amanha(10, 0), status='cancelado')
        self.client.post(reverse('agendamento_create'), self.dados_post(amanha(10, 0)))
        self.assertEqual(Agendamento.objects.count(), 2)

    def test_editar_nao_conflita_consigo_mesmo(self):
        ag = self.criar(amanha(10, 0))
        resposta = self.client.post(
            reverse('agendamento_update', args=[ag.pk]),
            self.dados_post(amanha(10, 0), observacoes='cortar na régua'))
        self.assertEqual(resposta.status_code, 302)
        ag.refresh_from_db()
        self.assertEqual(ag.observacoes, 'cortar na régua')

    def test_formulario_de_edicao_preenche_data_e_hora(self):
        ag = self.criar(amanha(14, 30))
        resposta = self.client.get(reverse('agendamento_update', args=[ag.pk]))
        self.assertContains(resposta, f'value="{texto(ag.inicio)}"')

    def test_excluir_agendamento(self):
        ag = self.criar()
        resposta = self.client.post(reverse('agendamento_delete', args=[ag.pk]))
        self.assertRedirects(resposta, reverse('agendamento_list'))
        self.assertFalse(Agendamento.objects.exists())


class AgendaViewTests(AgendaBase):
    def test_agenda_mostra_apenas_o_dia_escolhido(self):
        self.criar(amanha(10, 0))
        outro_dia = self.criar(amanha(10, 0) + timedelta(days=1), cliente=self.outro_cliente)
        dia = timezone.localtime(amanha()).date().isoformat()
        resposta = self.client.get(reverse('agendamento_list'), {'data': dia})
        self.assertEqual(list(resposta.context['agendamentos'])[0].cliente, self.cliente)
        self.assertEqual(len(resposta.context['agendamentos']), 1)
        self.assertNotIn(outro_dia, resposta.context['agendamentos'])

    def test_filtro_por_barbeiro(self):
        self.criar(amanha(10, 0))
        self.criar(amanha(10, 0), barbeiro=self.outro_barbeiro, cliente=self.outro_cliente)
        dia = timezone.localtime(amanha()).date().isoformat()
        resposta = self.client.get(
            reverse('agendamento_list'), {'data': dia, 'barbeiro': self.outro_barbeiro.pk})
        self.assertEqual(len(resposta.context['agendamentos']), 1)

    def test_data_invalida_cai_em_hoje(self):
        resposta = self.client.get(reverse('agendamento_list'), {'data': 'lixo', 'barbeiro': 'x'})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['dia'], timezone.localdate())

    def test_faturamento_conta_apenas_concluidos(self):
        self.criar(amanha(10, 0), status='concluido')
        self.criar(amanha(11, 0), status='agendado')
        dia = timezone.localtime(amanha()).date().isoformat()
        resposta = self.client.get(reverse('agendamento_list'), {'data': dia})
        self.assertEqual(resposta.context['faturamento'], '40,00')


class AgendamentoStatusTests(AgendaBase):
    def test_concluir_agendamento(self):
        ag = self.criar()
        resposta = self.client.post(reverse('agendamento_status', args=[ag.pk, 'concluido']))
        self.assertEqual(resposta.status_code, 302)
        ag.refresh_from_db()
        self.assertEqual(ag.status, 'concluido')

    def test_status_invalido_retorna_404(self):
        ag = self.criar()
        resposta = self.client.post(reverse('agendamento_status', args=[ag.pk, 'agendado']))
        self.assertEqual(resposta.status_code, 404)

    def test_status_nao_aceita_get(self):
        ag = self.criar()
        resposta = self.client.get(reverse('agendamento_status', args=[ag.pk, 'cancelado']))
        self.assertEqual(resposta.status_code, 405)

    def test_redirecionamento_externo_e_ignorado(self):
        ag = self.criar()
        resposta = self.client.post(
            reverse('agendamento_status', args=[ag.pk, 'cancelado']), {'next': 'https://evil.example/'})
        self.assertTrue(resposta.url.startswith(reverse('agendamento_list')))

    def test_painel_lista_proximos_agendamentos(self):
        self.criar()
        resposta = self.client.get(reverse('home'))
        self.assertEqual(len(resposta.context['proximos']), 1)


class ComunicacaoTests(AgendaBase):
    def com_email(self):
        self.cliente.email = 'ana@example.com'
        self.cliente.save()

    def test_mensagem_traz_os_dados_do_agendamento(self):
        ag = self.criar(amanha(10, 0))
        texto = montar_mensagem(ag)
        for esperado in ('Ana', 'Corte', 'Pedro', '10:00', '10:30', 'R$ 40,00',
                         timezone.localtime(ag.inicio).strftime('%d/%m/%Y')):
            self.assertIn(esperado, texto)

    def test_mensagem_de_cancelamento(self):
        ag = self.criar(status='cancelado')
        self.assertIn('foi cancelado', montar_mensagem(ag))

    def test_link_whatsapp(self):
        ag = self.criar()
        link = link_whatsapp(ag)
        self.assertTrue(link.startswith('https://wa.me/5511911112222?text='))
        self.assertNotIn(' ', link)

    def test_link_whatsapp_com_telefone_invalido(self):
        self.cliente.telefone = '123'
        self.cliente.save()
        self.assertIsNone(link_whatsapp(self.criar()))

    def test_criar_envia_email_automaticamente(self):
        self.com_email()
        resposta = self.client.post(reverse('agendamento_create'), self.dados_post(amanha(10, 0)))
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['ana@example.com'])
        self.assertIn('10:00', mail.outbox[0].body)

    def test_criar_sem_email_do_cliente_nao_envia(self):
        self.client.post(reverse('agendamento_create'), self.dados_post())
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Agendamento.objects.count(), 1)

    @override_settings(AGENDAMENTO_EMAIL_AUTOMATICO=False)
    def test_envio_automatico_pode_ser_desligado(self):
        self.com_email()
        self.client.post(reverse('agendamento_create'), self.dados_post())
        self.assertEqual(len(mail.outbox), 0)

    def test_falha_no_email_nao_impede_o_agendamento(self):
        self.com_email()
        with mock.patch('django.core.mail.EmailMessage.send', side_effect=OSError('sem rede')):
            resposta = self.client.post(reverse('agendamento_create'), self.dados_post())
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_tela_de_aviso_mostra_mensagem_e_link_do_whatsapp(self):
        ag = self.criar()
        resposta = self.client.get(reverse('agendamento_comunicar', args=[ag.pk]))
        self.assertContains(resposta, 'https://wa.me/5511911112222')
        self.assertContains(resposta, 'Corte')

    def test_reenviar_email_pela_tela_de_aviso(self):
        self.com_email()
        ag = self.criar()
        resposta = self.client.post(reverse('agendamento_comunicar', args=[ag.pk]))
        self.assertRedirects(resposta, reverse('agendamento_comunicar', args=[ag.pk]))
        self.assertEqual(len(mail.outbox), 1)

    def test_reenviar_sem_email_nao_envia(self):
        ag = self.criar()
        self.client.post(reverse('agendamento_comunicar', args=[ag.pk]))
        self.assertEqual(len(mail.outbox), 0)

    def test_tela_de_aviso_exige_login(self):
        ag = self.criar()
        self.client.logout()
        resposta = self.client.get(reverse('agendamento_comunicar', args=[ag.pk]))
        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse('login'), resposta.url)
