# ✂ Projeto Barbearia

Sistema web de gestão de barbearia com **Python** e **Django**: cadastro, busca, edição e exclusão de
**clientes**, **barbeiros** e **serviços**, com painel inicial e acesso restrito a funcionários.

> Resumo completo e tabela de funcionalidades: [`docs/FUNCIONALIDADES.md`](docs/FUNCIONALIDADES.md)

## Funcionalidades

- Login/logout; todas as telas exigem autenticação
- Painel inicial com totais, agendamentos de hoje e próximos horários
- **Agenda** por dia com filtro por barbeiro, bloqueio de conflitos de horário e status (confirmar, concluir, cancelar, falta)
- CRUD completo de clientes, barbeiros e serviços, com busca e paginação
- **Aviso ao cliente:** e-mail de confirmação automático ao agendar e tela com mensagem pronta para WhatsApp (link `wa.me`)
- Validação de telefone brasileiro (com formatação automática), preço e duração
- Django Admin (`/admin/`) com busca e filtros
- Configuração por variáveis de ambiente, testes automatizados e CI (GitHub Actions)

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.13+ | Linguagem |
| Django 6.1 | Framework web (models, views, forms, admin, templates) |
| python-dotenv | Leitura do arquivo `.env` |
| SQLite | Banco de dados local |
| HTML + CSS | Interface (template base + folha de estilos única) |
| GitHub Actions | Integração contínua (`check` + testes) |

## Estrutura

```
Projeto-Barbearia/
├── barbearia/
│   ├── migrations/
│   ├── static/barbearia/css/style.css   # Estilos compartilhados
│   ├── templates/
│   │   ├── barbearia/                   # base, home, list, form, confirm_delete
│   │   └── registration/login.html
│   ├── admin.py  forms.py  models.py  urls.py  views.py  tests.py
├── setup/                               # Configurações do projeto Django
├── docs/FUNCIONALIDADES.md
├── .github/workflows/ci.yml
├── .env.example                         # Modelo das variáveis de ambiente
├── manage.py
└── requirements.txt
```

## Como rodar

```bash
git clone https://github.com/teteu440/Projeto-Barbearia.git
cd Projeto-Barbearia

python -m venv venv
source venv/bin/activate          # Windows (PowerShell): .\venv\Scripts\Activate.ps1

pip install -r requirements.txt

cp .env.example .env              # Windows: copy .env.example .env  (edite a SECRET_KEY)

python manage.py migrate         # inclui a migração 0003 (agenda)
python manage.py createsuperuser  # usuário para entrar no sistema
python manage.py runserver
```

Acesse http://127.0.0.1:8000/ e entre com o usuário criado.

> Windows/PowerShell bloqueando a venv? Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

## Variáveis de ambiente (`.env`)

| Variável | Descrição | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django (obrigatória com `DEBUG=False`) | chave de desenvolvimento |
| `DEBUG` | Modo de depuração | `True` |
| `ALLOWED_HOSTS` | Domínios permitidos, separados por vírgula | vazio |
| `SECURE_SSL_REDIRECT` | Redireciona para HTTPS quando `DEBUG=False` | `True` |
| `BARBEARIA_NOME` | Nome usado nas mensagens aos clientes | `Barbearia` |
| `WHATSAPP_DDI` | Código do país para os links do WhatsApp | `55` |
| `AGENDAMENTO_EMAIL_AUTOMATICO` | Envia e-mail ao criar agendamento | `True` |
| `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | Envio de e-mail via SMTP | e-mail impresso no terminal |

Gerar uma chave: `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"`

## Rotas

| Rota | Descrição |
|---|---|
| `/` | Painel |
| `/login/`, `/logout/` | Autenticação |
| `/agenda/` | Agenda do dia (`?data=AAAA-MM-DD&barbeiro=<id>`) |
| `/agenda/<id>/avisar/` | Mensagem pronta para WhatsApp/e-mail |
| `/agenda/novo/`, `/agenda/<id>/editar/`, `/agenda/<id>/excluir/` | Cadastro, edição e exclusão de agendamentos |
| `/clientes/`, `/barbeiros/`, `/servicos/` | Listagem com busca e paginação |
| `/<recurso>/novo/` | Cadastro |
| `/<recurso>/<id>/editar/` | Edição |
| `/<recurso>/<id>/excluir/` | Exclusão (com confirmação) |
| `/admin/` | Painel administrativo do Django |

## Testes

```bash
python manage.py test
```

## Solução de problemas

- **`ZoneInfoNotFoundError`**: confira `TIME_ZONE = 'America/Sao_Paulo'` (maiúsculas corretas) e instale `tzdata`.
- **`ImproperlyConfigured: Defina a variável de ambiente SECRET_KEY`**: com `DEBUG=False` a chave é obrigatória.
- **Erro 400 (Bad Request) em produção**: adicione o domínio em `ALLOWED_HOSTS`.
- **`No module named 'dotenv'`**: rode `pip install -r requirements.txt` com a venv ativa.

## Trabalhando em equipe com Git

```bash
git pull                              # atualizar antes de começar
git checkout -b minha-feature         # criar uma branch
git add . && git commit -m "feat: descreva a mudança"
git push -u origin minha-feature      # enviar e abrir Pull Request
```

## Próximos passos sugeridos

Lembrete automático no dia anterior, relatórios (serviços mais vendidos, desempenho por barbeiro), horário de funcionamento/folgas e lembretes por e-mail/WhatsApp.
