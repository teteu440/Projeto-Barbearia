# Projeto Barbearia

Sistema web de gerenciamento de barbearia desenvolvido com **Python** e **Django**. Atualmente permite cadastrar e listar **clientes**, **barbeiros** e **serviços**.

---

## Sumário

1. [Funcionalidades](#funcionalidades)
2. [Tecnologias, pacotes e frameworks](#tecnologias-pacotes-e-frameworks)
3. [Estrutura do projeto](#estrutura-do-projeto)
4. [Pré-requisitos](#pré-requisitos)
5. [Tutorial passo a passo](#tutorial-passo-a-passo)
6. [Rotas disponíveis](#rotas-disponíveis)
7. [Comandos úteis](#comandos-úteis)
8. [Solução de problemas](#solução-de-problemas)
9. [Trabalhando em equipe com Git](#trabalhando-em-equipe-com-git)

---

## Funcionalidades

- Cadastro de clientes (nome, telefone, e-mail, data de nascimento)
- Cadastro de barbeiros (nome, telefone, e-mail, especialidade, data de contratação)
- Cadastro de serviços (nome, descrição, preço, duração em minutos)
- Listagem de clientes, barbeiros e serviços cadastrados
- Painel administrativo do Django (`/admin/`) com busca e edição dos registros
- Banco de dados SQLite (os dados ficam salvos no arquivo `db.sqlite3`)

---

## Tecnologias, pacotes e frameworks

| Tecnologia | Versão | Para que serve |
|---|---|---|
| [Python](https://www.python.org/) | 3.13 ou superior | Linguagem de programação |
| [Django](https://www.djangoproject.com/) | 6.1 | Framework web (models, views, forms, admin, templates) |
| [asgiref](https://pypi.org/project/asgiref/) | 3.12.1 | Dependência do Django (suporte ASGI) |
| [sqlparse](https://pypi.org/project/sqlparse/) | 0.6.0 | Dependência do Django (análise de SQL) |
| [tzdata](https://pypi.org/project/tzdata/) | 2026.3 | Banco de fusos horários (necessário no Windows) |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | última | Carrega variáveis do arquivo `.env` (ex: `SECRET_KEY`) |
| SQLite | embutido no Python | Banco de dados local |
| HTML + CSS | - | Templates das telas |
| Git / GitHub | - | Controle de versão |
| VS Code | - | IDE recomendada |

> **Importante:** o `settings.py` usa o pacote `python-dotenv`, mas ele pode não estar listado no `requirements.txt`. O tutorial abaixo já inclui a instalação dele.

---

## Estrutura do projeto

```
Projeto-Barbearia/
├── barbearia/                  # App principal
│   ├── migrations/             # Histórico de alterações do banco
│   ├── templates/
│   │   └── barbearia/
│   │       ├── cadastro.html   # Tela de cadastro (cliente, barbeiro, serviço)
│   │       └── listagem.html   # Tela de listagem
│   ├── admin.py                # Registro dos models no admin
│   ├── forms.py                # Formulários (ClienteForm, BarbeiroForm, ServicoForm)
│   ├── models.py               # Models (Cliente, Barbeiro, Servico)
│   ├── urls.py                 # Rotas do app
│   └── views.py                # Lógica das telas
├── setup/                      # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .env                        # Variáveis secretas (NÃO vai pro GitHub)
├── .gitignore
├── db.sqlite3                  # Banco de dados local
├── manage.py                   # Utilitário de comandos do Django
├── requirements.txt            # Dependências do projeto
└── README.md
```

---

## Pré-requisitos

Instale estes programas **antes** de começar:

1. **Python 3.13 ou superior** — https://www.python.org/downloads/
   - Na instalação no Windows, marque a opção **"Add Python to PATH"**.
   - Confirme no terminal: `python --version`
2. **Git** — https://git-scm.com/downloads
   - Confirme no terminal: `git --version`
3. **Visual Studio Code** — https://code.visualstudio.com/
4. Uma conta no **GitHub** — https://github.com/

---

## Tutorial passo a passo

### Passo 1 — Baixar o projeto do GitHub

Você pode baixar de duas formas. **A opção A (clonar) é a recomendada**, pois permite enviar alterações depois.

#### Opção A — Clonar com Git (recomendado)

1. Escolha uma pasta onde ficará o projeto (ex: `Área de Trabalho`).
2. Abra o terminal nessa pasta (no Windows: clique com o botão direito na pasta > **Abrir no Terminal**).
3. Rode:

```bash
git clone https://github.com/teteu440/Projeto-Barbearia.git
```

4. Entre na pasta do projeto:

```bash
cd Projeto-Barbearia
```

#### Opção B — Baixar o ZIP

1. Acesse https://github.com/teteu440/Projeto-Barbearia
2. Clique no botão verde **Code** > **Download ZIP**.
3. Extraia o ZIP **uma única vez**, em uma pasta que você vai usar sempre.

**Atenção:** extrair o ZIP várias vezes cria pastas duplicadas (`Projeto-Barbearia-1`, `Projeto-Barbearia-2`...). Use sempre a mesma pasta para não se perder.

---

### Passo 2 — Abrir o projeto no VS Code

1. Abra o **VS Code**.
2. Vá em **Arquivo > Abrir Pasta...** e selecione a pasta `Projeto-Barbearia` (a que contém o `manage.py`).
3. Se o VS Code perguntar *"Você confia nos autores desta pasta?"*, clique em **Sim, eu confio**.

Ou, pelo terminal, dentro da pasta do projeto:

```bash
code .
```

#### Extensões recomendadas do VS Code

Abra o painel de extensões (`Ctrl+Shift+X`) e instale:

- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **Django** (Baptiste Darthenay) — realce de sintaxe dos templates

#### Abrir o terminal integrado

No VS Code, aperte `` Ctrl+` `` (ou menu **Terminal > Novo Terminal**). Todos os comandos abaixo são executados nesse terminal, **dentro da pasta do projeto**.

Para confirmar que está na pasta certa, rode:

```powershell
dir
```

Você deve ver o arquivo `manage.py` na lista.

---

### Passo 3 — Criar o ambiente virtual (venv)

O ambiente virtual isola as bibliotecas do projeto das demais do seu computador.

```bash
python -m venv venv
```

---

### Passo 4 — Ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Quando der certo, o terminal passa a mostrar `(venv)` no início da linha:

```
(venv) PS C:\...\Projeto-Barbearia>
```

> Se o PowerShell bloquear com o erro *"a execução de scripts foi desabilitada neste sistema"*, rode este comando e tente ativar de novo:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

---

### Passo 5 — Selecionar o interpretador no VS Code

1. Aperte `Ctrl+Shift+P`.
2. Digite e selecione **Python: Select Interpreter**.
3. Escolha o que tem `venv` no caminho (ex: `.\venv\Scripts\python.exe`).

Isso evita avisos falsos de "import não resolvido" no editor.

---

### Passo 6 — Instalar as dependências

Com a venv ativa `(venv)`:

```bash
pip install -r requirements.txt
pip install python-dotenv
```

Confirme o que foi instalado:

```bash
pip list
```

> **Dica:** para registrar o `python-dotenv` no `requirements.txt` e evitar esse passo extra para os próximos colegas:
> ```bash
> pip freeze > requirements.txt
> ```

---

### Passo 7 — Criar o arquivo `.env`

O projeto lê a chave secreta do Django de um arquivo `.env` (que **não** é enviado ao GitHub por segurança).

1. Na raiz do projeto (mesma pasta do `manage.py`), crie um arquivo chamado `.env`.
2. Coloque dentro dele:

```
SECRET_KEY=troque-por-uma-chave-secreta-qualquer-e-longa
```

Para gerar uma chave segura, rode:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

e copie o resultado para o `.env`.

---

### Passo 8 — Conferir o fuso horário

Abra `setup/settings.py` e confirme que a linha está **exatamente** assim (com as letras maiúsculas corretas):

```python
TIME_ZONE = 'America/Sao_Paulo'
```

Se estiver `'america/Sao_paulo'` (minúsculo), o Django quebra com o erro `ZoneInfoNotFoundError`. Corrija e salve.

---

### Passo 9 — Criar as tabelas do banco de dados (migrações)

```bash
python manage.py makemigrations barbearia
python manage.py migrate
```

Você deve ver linhas como `Applying barbearia.0001_initial... OK`.

---

### Passo 10 — (Opcional) Criar um superusuário para o admin

```bash
python manage.py createsuperuser
```

Informe nome de usuário, e-mail e senha quando solicitado.

---

### Passo 11 — Rodar o servidor

```bash
python manage.py runserver
```

Se tudo estiver certo, aparece:

```
Starting WSGI development server at http://127.0.0.1:8000/
```

**Deixe esse terminal aberto** — se você fechar ou apertar `Ctrl+C`, o site para de funcionar.

---

### Passo 12 — Acessar o sistema no navegador

Abra o navegador e digite a URL na **barra de endereço** (no topo da janela, e não na caixa de busca do Google):

| Tela | URL |
|---|---|
| Página inicial | http://127.0.0.1:8000/ |
| Cadastro de cliente | http://127.0.0.1:8000/cadastro/ |
| Cadastro de barbeiro | http://127.0.0.1:8000/cadastro/barbeiro/ |
| Cadastro de serviço | http://127.0.0.1:8000/cadastro/servico/ |
| Lista de clientes | http://127.0.0.1:8000/clientes/ |
| Lista de barbeiros | http://127.0.0.1:8000/barbeiros/ |
| Lista de serviços | http://127.0.0.1:8000/servicos/ |
| Painel admin | http://127.0.0.1:8000/admin/ |

Para parar o servidor, aperte `Ctrl+C` no terminal.

---

## Rotas disponíveis

| Rota | View | Nome |
|---|---|---|
| `/` | `index` | - |
| `/cadastro/` | `cadastro_cliente` | `cadastro_cliente` |
| `/cadastro/barbeiro/` | `cadastro_barbeiro` | `cadastro_barbeiro` |
| `/cadastro/servico/` | `cadastro_servico` | `cadastro_servico` |
| `/clientes/` | `listar_clientes` | `listar_clientes` |
| `/barbeiros/` | `listar_barbeiros` | `listar_barbeiros` |
| `/servicos/` | `listar_servicos` | `listar_servicos` |
| `/admin/` | Django Admin | - |

---

## Comandos úteis

| Comando | O que faz |
|---|---|
| `python manage.py runserver` | Inicia o servidor de desenvolvimento |
| `python manage.py makemigrations barbearia` | Gera migrações após alterar `models.py` |
| `python manage.py migrate` | Aplica as migrações no banco |
| `python manage.py createsuperuser` | Cria um usuário administrador |
| `python manage.py check` | Verifica se há erros de configuração |
| `pip install -r requirements.txt` | Instala as dependências |
| `pip freeze > requirements.txt` | Atualiza a lista de dependências |
| `deactivate` | Sai do ambiente virtual |

---

## Solução de problemas

| Erro | Causa provável | Solução |
|---|---|---|
| `ImportError: Couldn't import Django` | venv não está ativa ou Django não instalado | Ative a venv (Passo 4) e rode `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'dotenv'` | Falta o `python-dotenv` | `pip install python-dotenv` |
| `no such table: barbearia_cliente` | Migrações não aplicadas | `python manage.py makemigrations barbearia` e `python manage.py migrate` |
| `ZoneInfoNotFoundError: ... america/Sao_paulo` | `TIME_ZONE` escrito errado | Use `'America/Sao_Paulo'` no `settings.py` |
| `TemplateDoesNotExist` | Pasta `templates` com nome errado | A pasta deve se chamar `templates` (plural) em `barbearia/templates/barbearia/` |
| `ImportError: cannot import name 'cadastro_cliente'` | Arquivo `views.py` desatualizado/não salvo | Salve o arquivo e confira com `type barbearia\views.py` |
| `ERR_CONNECTION_REFUSED` no navegador | Servidor não está rodando | Rode `python manage.py runserver` e deixe o terminal aberto |
| A URL abre uma pesquisa do Google | URL digitada na caixa de busca | Digite na barra de endereço, no topo do navegador |
| `Page not found (404)` em `/cadastro/` | `urls.py` do app desatualizado | Confira as rotas em `barbearia/urls.py` |
| `A server error occurred` (mensagem genérica) | Erro oculto; veja o terminal do `runserver` | Leia o traceback no terminal para achar a causa real |
| `execução de scripts foi desabilitada` | Política do PowerShell | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `error: remote origin already exists` | Remoto já configurado | Ignore; não precisa rodar `git remote add` de novo |

---

## Trabalhando em equipe com Git

### Rotina diária

```bash
# 1. Antes de começar, atualize seu código local
git pull

# 2. Trabalhe, teste e salve suas alterações

# 3. Veja o que mudou
git status

# 4. Adicione e registre as alterações
git add .
git commit -m "Descreva o que você fez"

# 5. Envie para o GitHub
git push
```

### Se o `git push` for rejeitado (`non-fast-forward`)

Significa que alguém (ou você, em outra máquina) enviou alterações antes. Resolva assim:

```bash
git pull
git push
```

Se aparecer `CONFLICT`, abra os arquivos indicados, resolva os trechos marcados com `<<<<<<<`, `=======` e `>>>>>>>`, depois:

```bash
git add .
git commit -m "Resolve conflito"
git push
```

### O que NÃO enviar ao GitHub

Confirme que o `.gitignore` contém, no mínimo:

```
venv/
__pycache__/
*.pyc
.env
db.sqlite3
```

Assim você não envia a venv (pesada), senhas ou o banco de dados local.

---


Repositório: https://github.com/teteu440/Projeto-Barbearia
