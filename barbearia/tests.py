"""Suite de testes automatizados (Django TestCase) - Plano de Testes da Barbearia.

Cada teste corresponde a um caso (CT-XX) da tabela do relatorio.
Executar com:  python manage.py test
Os testes marcados [REPROVA] descrevem o comportamento ESPERADO e falham
enquanto o defeito correspondente nao for corrigido.
"""
from datetime import date, timedelta

from django.test import TestCase, Client
from django.urls import reverse

from .models import Cliente, Barbeiro, Servico


class ClienteTests(TestCase):
    url = 'cadastro_cliente'

    def post(self, **dados):
        base = {'nome': 'Joao Silva', 'telefone': '(84) 99999-0000'}
        base.update(dados)
        return self.client.post(reverse(self.url), base)

    def test_ct01_cadastro_valido(self):
        r = self.post(email='joao@email.com', data_nascimento='1990-05-15')
        self.assertRedirects(r, reverse(self.url))
        self.assertEqual(Cliente.objects.count(), 1)
        r = self.client.get(reverse(self.url))
        self.assertContains(r, 'Cliente cadastrado com sucesso!')

    def test_ct02_nome_vazio(self):
        r = self.post(nome='')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Este campo é obrigatório.')
        self.assertEqual(Cliente.objects.count(), 0)

    def test_ct03_email_invalido(self):
        r = self.post(email='joao@')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_ct04_nome_com_151_caracteres(self):
        r = self.post(nome='A' * 151)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_ct05_telefone_com_letras_REPROVA(self):
        r = self.post(telefone='abc')
        self.assertEqual(r.status_code, 200)       # deve reexibir o formulario
        self.assertEqual(Cliente.objects.count(), 0)

    def test_ct06_nascimento_futuro_REPROVA(self):
        futuro = (date.today() + timedelta(days=365)).isoformat()
        r = self.post(data_nascimento=futuro)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_ct07_telefone_duplicado_REPROVA(self):
        self.post()
        r = self.post(nome='Maria Souza')          # mesmo telefone
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_ct08_xss_e_escapado_na_listagem(self):
        self.post(nome='<script>alert(1)</script>')
        r = self.client.get(reverse('listar_clientes'))
        self.assertNotContains(r, '<script>alert(1)</script>')
        self.assertContains(r, '&lt;script&gt;')


class BarbeiroTests(TestCase):
    url = 'cadastro_barbeiro'

    def test_ct09_cadastro_valido_sem_especialidade(self):
        r = self.client.post(reverse(self.url),
                             {'nome': 'Carlos', 'telefone': '(84) 98888-1111'})
        self.assertRedirects(r, reverse(self.url))
        r = self.client.get(reverse('listar_barbeiros'))
        self.assertContains(r, 'Carlos')
        self.assertContains(r, '<td>-</td>', html=True)

    def test_ct10_telefone_com_21_caracteres(self):
        r = self.client.post(reverse(self.url),
                             {'nome': 'Carlos', 'telefone': '9' * 21})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Barbeiro.objects.count(), 0)


class ServicoTests(TestCase):
    url = 'cadastro_servico'

    def post(self, **dados):
        base = {'nome': 'Corte', 'preco': '35.00', 'duracao_minutos': '30'}
        base.update(dados)
        return self.client.post(reverse(self.url), base)

    def test_ct11_cadastro_valido(self):
        r = self.post()
        self.assertRedirects(r, reverse(self.url))
        self.assertEqual(Servico.objects.count(), 1)

    def test_ct12_preco_negativo_REPROVA(self):
        r = self.post(preco='-10.00')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Servico.objects.count(), 0)

    def test_ct13_duracao_zero_REPROVA(self):
        r = self.post(duracao_minutos='0')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Servico.objects.count(), 0)

    def test_ct14_duracao_negativa(self):
        r = self.post(duracao_minutos='-5')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Servico.objects.count(), 0)

    def test_ct15_preco_acima_do_limite(self):
        r = self.post(preco='1234567.00')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Servico.objects.count(), 0)


class ListagemENavegacaoTests(TestCase):
    def test_ct16_listagem_vazia(self):
        for nome in ('listar_clientes', 'listar_barbeiros', 'listar_servicos'):
            r = self.client.get(reverse(nome))
            self.assertContains(r, 'Nenhum registro cadastrado ainda.')

    def test_ct17_listagem_ordenada_por_nome(self):
        Cliente.objects.create(nome='Zeca', telefone='1')
        Cliente.objects.create(nome='Ana', telefone='2')
        r = self.client.get(reverse('listar_clientes'))
        c = r.content.decode()
        self.assertLess(c.index('Ana'), c.index('Zeca'))

    def test_ct18_preco_formatado_em_ptbr_REPROVA(self):
        Servico.objects.create(nome='Corte', preco='35.00', duracao_minutos=30)
        r = self.client.get(reverse('listar_servicos'))
        self.assertContains(r, '35,00')

    def test_ct19_link_para_listagens_no_cadastro_REPROVA(self):
        r = self.client.get(reverse('cadastro_cliente'))
        self.assertContains(r, reverse('listar_clientes'))

    def test_ct20_post_sem_csrf_e_bloqueado(self):
        c = Client(enforce_csrf_checks=True)
        r = c.post(reverse('cadastro_cliente'),
                   {'nome': 'X', 'telefone': '1'})
        self.assertEqual(r.status_code, 403)
        self.assertEqual(Cliente.objects.count(), 0)
