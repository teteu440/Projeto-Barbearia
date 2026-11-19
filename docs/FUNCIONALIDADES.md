# Funcionalidades e resumo do projeto

## Resumo

O **Projeto Barbearia** é um sistema web de gestão de barbearia feito com **Python 3.13 e Django 6.1**.
Ele centraliza o cadastro de **clientes**, **barbeiros** e **serviços** (com preço e duração) e a **agenda de
agendamentos**, oferecendo painel inicial, busca, paginação, edição e exclusão. O acesso é restrito a funcionários autenticados e
o painel administrativo do Django complementa a operação.

É um projeto de base sólida, pensado para evoluir para **agendamentos, controle financeiro e relatórios**.

## Tabela de funcionalidades

| # | Módulo | Funcionalidade | Rota | Status |
|---|--------|----------------|------|:------:|
| 1 | Acesso | Login / logout de funcionários | `/login/`, `/logout/` | ✅ |
| 2 | Acesso | Todas as telas protegidas por login | — | ✅ |
| 3 | Painel | Totais de clientes, barbeiros e serviços + últimos clientes | `/` | ✅ |
| 4 | Clientes | Cadastrar (nome, telefone, e-mail, nascimento) | `/clientes/novo/` | ✅ |
| 5 | Clientes | Listar com busca e paginação | `/clientes/` | ✅ |
| 6 | Clientes | Editar | `/clientes/<id>/editar/` | ✅ |
| 7 | Clientes | Excluir (com confirmação) | `/clientes/<id>/excluir/` | ✅ |
| 8 | Barbeiros | Cadastrar (nome, telefone, e-mail, especialidade, contratação) | `/barbeiros/novo/` | ✅ |
| 9 | Barbeiros | Listar com busca e paginação | `/barbeiros/` | ✅ |
| 10 | Barbeiros | Editar / excluir | `/barbeiros/<id>/editar/`, `/excluir/` | ✅ |
| 11 | Serviços | Cadastrar (nome, descrição, preço, duração) | `/servicos/novo/` | ✅ |
| 12 | Serviços | Listar com busca e paginação (preço em R$) | `/servicos/` | ✅ |
| 13 | Serviços | Editar / excluir | `/servicos/<id>/editar/`, `/excluir/` | ✅ |
| 14 | Validações | Telefone brasileiro (DDD + 8/9 dígitos) com formatação automática | formulários | ✅ |
| 15 | Validações | Preço > 0 e duração ≥ 1 minuto | formulários | ✅ |
| 16 | Administração | Django Admin com busca, filtros e histórico por data | `/admin/` | ✅ |
| 17 | Infra | Configuração por variáveis de ambiente (`.env`) | — | ✅ |
| 18 | Qualidade | Testes automatizados + CI no GitHub Actions | — | ✅ |
| 19 | Agenda | Agenda por dia, com navegação (anterior / próximo / hoje) e filtro por barbeiro | `/agenda/` | ✅ |
| 20 | Agenda | Agendar cliente × barbeiro × serviço (término calculado pela duração) | `/agenda/novo/` | ✅ |
| 21 | Agenda | Bloqueio de conflitos de horário (barbeiro e cliente) e de datas passadas | formulário | ✅ |
| 22 | Agenda | Status: agendado, confirmado, concluído, cancelado, não compareceu (ações rápidas) | `/agenda/<id>/status/<status>/` | ✅ |
| 23 | Agenda | Editar / excluir agendamento | `/agenda/<id>/editar/`, `/excluir/` | ✅ |
| 24 | Agenda | Valor do serviço "congelado" no agendamento (preserva o histórico) | — | ✅ |
| 25 | Painel | Agendamentos de hoje e próximos agendamentos | `/` | ✅ |
| 26 | Agenda | Faturamento do dia (apenas atendimentos concluídos) | `/agenda/` | ✅ |
| 27 | Relatórios | Serviços mais vendidos, desempenho por barbeiro, faturamento por período | — | 🔜 sugerido |
| 28 | Notificações | E-mail de confirmação automático ao agendar (se o cliente tiver e-mail) | — | ✅ |
| 29 | Notificações | Tela "Avisar cliente": mensagem pronta, botão de WhatsApp, reenvio de e-mail e copiar | `/agenda/<id>/avisar/` | ✅ |
| 30 | Notificações | Mensagem de cancelamento (mesma tela) | `/agenda/<id>/avisar/` | ✅ |
| 31 | Notificações | Lembrete automático 1 dia antes (exige tarefa agendada) | — | 🔜 sugerido |
| 32 | Agenda | Horário de funcionamento e folgas dos barbeiros | — | 🔜 sugerido |

## Modelos de dados

| Modelo | Campos |
|--------|--------|
| `Cliente` | nome, telefone, e-mail (opcional), data de nascimento (opcional), criado em |
| `Barbeiro` | nome, telefone, e-mail (opcional), especialidade, data de contratação, criado em |
| `Servico` | nome, descrição, preço (decimal), duração em minutos, criado em |
| `Agendamento` | cliente, barbeiro, serviço, início, término (automático), valor (automático), status, observações, criado em |
