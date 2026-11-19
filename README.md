# ✂ Projeto Barbearia

Sistema web de gestão para barbearias, desenvolvido com **Python** e **Django**. Reúne o cadastro de clientes, barbeiros e serviços e uma **agenda de horários** com controle de conflitos, tudo em uma interface simples e com acesso restrito aos funcionários.

---

## Sumário

1. [Funcionalidades](#funcionalidades)
2. [Tecnologias](#tecnologias)
3. [Estrutura do projeto](#estrutura-do-projeto)
4. [Modelo de dados](#modelo-de-dados)
5. [Instalação e execução](#instalação-e-execução)
6. [Primeiro acesso](#primeiro-acesso)
7. [Configuração (.env)](#configuração-env)
8. [Como usar a agenda](#como-usar-a-agenda)
9. [Rotas](#rotas)
10. [Testes](#testes)
11. [Solução de problemas](#solução-de-problemas)
12. [Trabalhando em equipe com Git](#trabalhando-em-equipe-com-git)
13. [Próximos passos](#próximos-passos)

---

## Funcionalidades

| Módulo | O que o sistema faz |
|---|---|
| **Acesso** | Login e logout de funcionários. Todas as telas exigem autenticação |
| **Painel** | Totais de clientes, barbeiros e serviços, agendamentos de hoje e próximos horários |
| **Clientes** | Cadastrar, listar (com busca e paginação), editar e excluir |
| **Barbeiros** | Cadastrar, listar (com busca e paginação), editar e excluir |
| **Serviços** | Cadastrar, listar (com busca e paginação), editar e excluir, com preço em R$ e duração em minutos |
| **Agenda** | Agenda por dia com navegação (anterior, próximo, hoje) e filtro por barbeiro |
| **Agendamentos** | Agendar cliente × barbeiro × serviço; o horário de término é calculado pela duração do serviço |
| **Conflitos** | Bloqueia horários sobrepostos do mesmo barbeiro ou do mesmo cliente e datas que já passaram |
| **Status** | Agendado, confirmado, concluído, cancelado e não compareceu, com botões de ação rápida |
| **Faturamento** | Soma do dia considerando apenas os atendimentos concluídos |
| **Histórico de valores** | O preço do serviço é guardado no agendamento; mudar o preço depois não altera o histórico |
| **Avisar cliente** | Tela com a mensagem pronta do agendamento, botão para abrir o WhatsApp com o texto preenchido e botão para copiar a mensagem |
| **Validações** | Telefone brasileiro (DDD + 8 ou 9 dígitos) com formatação automática; preço maior que zero; duração de pelo menos 1 minuto |
| **Administração** | Painel do Django (`/admin/`) com busca, filtros e histórico por data |

---

## Tecnologias

| Tecnologia | Para que serve |
|---|---|
| [Python](https://www.python.org/) 3.13+ | Linguagem de programação |
| [Django](https://www.djangoproject.com/) 6.1 | Framework web (models, views, forms, admin e templates) |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Leitura das variáveis do arquivo `.env` |
| asgiref, sqlparse, tzdata | Dependências do Django (tzdata é necessário no Windows) |
| SQLite | Banco de dados local (arquivo `db.sqlite3`) |
| HTML + CSS | Interface: um template base e uma folha de estilos única |
| GitHub Actions | Integração contínua: verificação do projeto e execução dos testes |

---

## Estrutura do projeto

```
Projeto-Barbearia/
├── barbearia/                          # App principal
│   ├── migrations/                     # Histórico de alterações do banco
│   ├── static/barbearia/css/style.css  # Estilos compartilhados
│   ├── templates/
│   │   ├── barbearia/                  # base, home, list, form, agenda, comunicar, confirm_delete
│   │   └── registration/login.html     # Tela de login
│   ├── admin.py                        # Configuração do painel administrativo
│   ├── forms.py                        # Formulários e validações
│   ├── models.py                       # Cliente, Barbeiro, Servico, Agendamento
│   ├── notificacoes.py                 # Montagem das mensagens ao cliente
│   ├── tests.py                        # Testes automatizados
│   ├── urls.py                         # Rotas do app
│   └── views.py                        # Lógica das telas
├── setup/                              # Configurações do projeto Django
├── docs/FUNCIONALIDADES.md             # Resumo e tabela de funcionalidades
├── .github/workflows/ci.yml            # Integração contínua
├── .env.example                        # Modelo do arquivo de variáveis de ambiente
├── manage.py                           # Utilitário de comandos do Django
└── requirements.txt                    # Dependências do projeto
```

---

## Modelo de dados

| Modelo | Campos |
|---|---|
| `Cliente` | nome, telefone, e-mail (opcional), data de nascimento (opcional), cadastrado em |
| `Barbeiro` | nome, telefone, e-mail (opcional), especialidade, data de contratação, cadastrado em |
| `Servico` | nome, descrição, preço, duração em minutos, cadastrado em |
| `Agendamento` | cliente, barbeiro, serviço, início, término (automático), valor (automático), status, observações, cadastrado em |

Clientes, barbeiros e serviços que já possuem agendamentos **não podem ser excluídos**, para preservar o histórico.

---

## Instalação e execução

### Pré-requisitos

- [Python 3.13 ou superior](https://www.python.org/downloads/) (no Windows, marque **Add Python to PATH** na instalação)
- [Git](https://git-scm.com/downloads)
- Um editor de código, como o [VS Code](https://code.visualstudio.com/)

### Passo a passo

**1. Baixe o projeto**

```bash
git clone https://github.com/teteu440/Projeto-Barbearia.git
cd Projeto-Barbearia
```

**2. Crie e ative o ambiente virtual**

```bash
python -m venv venv
```

| Sistema | Comando de ativação |
|---|---|
| Windows (PowerShell) | `.\venv\Scripts\Activate.ps1` |
| Windows (CMD) | `venv\Scripts\activate.bat` |
| Linux / macOS | `source venv/bin/activate` |

Quando der certo, o terminal mostra `(venv)` no início da linha.

> Se o PowerShell bloquear a execução de scripts, rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e tente de novo.

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Crie o arquivo `.env`**

Copie o modelo e edite a `SECRET_KEY`:

```bash
# Linux / macOS
cp .env.example .env
# Windows
copy .env.example .env
```

Para gerar uma chave segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

**5. Crie o banco de dados**

```bash
python manage.py migrate
```

**6. Crie o usuário de acesso**

```bash
python manage.py createsuperuser
```

Informe um nome de usuário e uma senha (ela não aparece na tela enquanto você digita).

**7. Inicie o servidor**

```bash
python manage.py runserver
```

Acesse http://127.0.0.1:8000/ e entre com o usuário criado.

---

## Primeiro acesso

Para começar a usar o sistema, cadastre nesta ordem:

1. **Serviços** (por exemplo, Corte, 30 min, R$ 40,00)
2. **Barbeiros**
3. **Clientes**
4. **Agendamentos**, na aba **Agenda**

Outros funcionários podem ser criados em `/admin/`, na seção **Usuários**. Qualquer usuário ativo consegue entrar no sistema; apenas quem for marcado como **Membro da equipe** acessa o `/admin/`.

---

## Configuração (.env)

O arquivo `.env` fica na raiz do projeto, ao lado do `manage.py`. Ele **não é enviado ao GitHub**, pois contém dados secretos.

| Variável | Descrição | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django. Obrigatória quando `DEBUG=False` | chave de desenvolvimento |
| `DEBUG` | Modo de depuração. Use `False` em produção | `True` |
| `ALLOWED_HOSTS` | Domínios permitidos, separados por vírgula | vazio |
| `SECURE_SSL_REDIRECT` | Redireciona para HTTPS quando `DEBUG=False` | `True` |
| `BARBEARIA_NOME` | Nome da barbearia usado nas mensagens aos clientes | `Barbearia` |
| `WHATSAPP_DDI` | Código do país usado nos links do WhatsApp | `55` |

Exemplo:

```
SECRET_KEY=troque-por-uma-chave-longa-e-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
BARBEARIA_NOME=Minha Barbearia
```

---

## Como usar a agenda

1. Abra a aba **Agenda**. A tela mostra os agendamentos do dia, e as setas ← → navegam entre os dias. O filtro permite ver um barbeiro específico.
2. Clique em **+ Novo agendamento**, escolha cliente, barbeiro, serviço e data/hora, e salve.
3. O sistema recusa o agendamento se o barbeiro ou o cliente já tiver outro horário no mesmo período, ou se a data já passou. Horários seguidos, como 10:00–10:30 e depois 10:30–11:00, são aceitos.
4. Ao salvar, abre a tela **Avisar o cliente**, com a mensagem pronta. Use **Enviar por WhatsApp** para abrir a conversa com o texto já preenchido, ou **Copiar mensagem**. Essa tela também pode ser aberta depois, pelo botão **Avisar** de cada linha da agenda.
5. Pelos botões da linha, mude o status: **Confirmar**, **Concluir**, **Faltou** ou **Cancelar**. Cancelamentos e faltas liberam o horário.
6. O faturamento exibido no topo soma somente os atendimentos **concluídos** do dia.

---

## Rotas

| Rota | Descrição |
|---|---|
| `/` | Painel inicial |
| `/login/`, `/logout/` | Autenticação |
| `/agenda/` | Agenda do dia (`?data=AAAA-MM-DD&barbeiro=<id>`) |
| `/agenda/novo/` | Novo agendamento |
| `/agenda/<id>/editar/`, `/agenda/<id>/excluir/` | Editar e excluir agendamento |
| `/agenda/<id>/avisar/` | Mensagem pronta para o cliente |
| `/clientes/`, `/barbeiros/`, `/servicos/` | Listagens com busca e paginação |
| `/clientes/novo/`, `/barbeiros/novo/`, `/servicos/novo/` | Cadastros |
| `/<recurso>/<id>/editar/`, `/<recurso>/<id>/excluir/` | Edição e exclusão |
| `/admin/` | Painel administrativo do Django |

---

## Testes

```bash
python manage.py test
```

Os testes cobrem login, CRUD, busca, paginação, validações, conflitos de horário, mudanças de status, preço histórico e as mensagens ao cliente. A integração contínua (GitHub Actions) roda a verificação do projeto e os testes a cada push.

---

## Solução de problemas

| Problema | Solução |
|---|---|
| `ZoneInfoNotFoundError` | Confira `TIME_ZONE = 'America/Sao_Paulo'` (com as maiúsculas corretas) em `setup/settings.py` e instale o `tzdata` |
| `No module named 'dotenv'` ou `'django'` | Ative a venv e rode `pip install -r requirements.txt` |
| `ImproperlyConfigured: Defina a variável de ambiente SECRET_KEY` | Com `DEBUG=False`, a `SECRET_KEY` é obrigatória no `.env` |
| Erro 400 (Bad Request) em produção | Adicione o domínio em `ALLOWED_HOSTS` |
| `no such table` | Rode `python manage.py migrate` |
| Esqueci a senha do usuário | Rode `python manage.py changepassword <usuario>` |
| O PowerShell não ativa a venv | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |

---

## Trabalhando em equipe com Git

```bash
git pull                                   # atualizar antes de começar
git checkout -b minha-feature              # criar uma branch
git add .
git commit -m "feat: descreva a mudança"
git push -u origin minha-feature           # enviar e abrir um Pull Request
```

Depois de atualizar o projeto, quem já o utiliza deve rodar `pip install -r requirements.txt` e `python manage.py migrate`.

---

