##  Como Executar o Projeto Localmente

Siga o passo a passo abaixo para clonar, configurar e rodar a aplicação na sua máquina.

### Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:
* [Python 3.10+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

---

### 1. Clonar o repositório
* Use os Comandos Ctrl, Shift e P para abrir a guia de seleções
* Pesquise "CLONE"
* Insira a seguinte URL: https://github.com/teteu440/Projeto-Barbearia.git

---

### 2. Configuração Local
* Criar e ativar o venv: python -m venv ./venv e depois venv\Scripts\activate
* Instalar dependências: pip install -r requirements.txt, django e dotenv
* Criar o banco: python manage.py migrate
* Rodar: python manage.py runserver
