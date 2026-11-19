"""Mensagens de confirmação de agendamento (e-mail e WhatsApp)."""
import logging
import re
from urllib.parse import quote

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.formats import date_format

from .models import Agendamento

logger = logging.getLogger(__name__)


def _formatar_valor(valor):
    return f'R$ {valor:.2f}'.replace('.', ',')


def _horarios(agendamento):
    return timezone.localtime(agendamento.inicio), timezone.localtime(agendamento.fim)


def montar_assunto(agendamento):
    inicio, _ = _horarios(agendamento)
    return f'{settings.BARBEARIA_NOME}: seu horário em {inicio:%d/%m} às {inicio:%H:%M}'


def montar_mensagem(agendamento):
    inicio, fim = _horarios(agendamento)
    nome = agendamento.cliente.nome.split()[0]
    barbearia = settings.BARBEARIA_NOME
    data = date_format(inicio, 'l, d/m/Y')

    if agendamento.status == Agendamento.Status.CANCELADO:
        return (
            f'Olá, {nome}! Seu agendamento de {agendamento.servico.nome} em {data} '
            f'às {inicio:%H:%M} na {barbearia} foi cancelado.\n\n'
            'Para reagendar, é só nos chamar.'
        )

    situacao = 'confirmado' if agendamento.status == Agendamento.Status.CONFIRMADO else 'agendado'
    return (
        f'Olá, {nome}! Seu horário na {barbearia} está {situacao}:\n\n'
        f'✂ Serviço: {agendamento.servico.nome}\n'
        f'👤 Barbeiro: {agendamento.barbeiro.nome}\n'
        f'📅 Data: {data}\n'
        f'🕒 Horário: {inicio:%H:%M} às {fim:%H:%M}\n'
        f'💰 Valor: {_formatar_valor(agendamento.preco)}\n\n'
        'Se precisar remarcar ou cancelar, é só responder esta mensagem. Até lá!'
    )


def link_whatsapp(agendamento):
    """Link 'clique para conversar' com a mensagem pronta, ou None se o telefone for inválido."""
    digitos = re.sub(r'\D', '', agendamento.cliente.telefone or '')
    if len(digitos) not in (10, 11):
        return None
    texto = quote(montar_mensagem(agendamento))
    return f'https://wa.me/{settings.WHATSAPP_DDI}{digitos}?text={texto}'


def enviar_email(agendamento):
    """Envia a confirmação por e-mail. Devolve True se enviou, False se não deu."""
    destino = agendamento.cliente.email
    if not destino:
        return False
    try:
        enviados = send_mail(
            montar_assunto(agendamento),
            montar_mensagem(agendamento),
            None,  # usa DEFAULT_FROM_EMAIL
            [destino],
        )
    except Exception:  # falha de rede/SMTP não pode quebrar o agendamento
        logger.exception('Falha ao enviar e-mail do agendamento %s', agendamento.pk)
        return False
    return enviados > 0
