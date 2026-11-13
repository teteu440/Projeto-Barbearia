Resumo do fluxo ao clonar o projeto em outra máquina:

1° Clonar o projeto na respectiva IDE(VS Code);
2° Criar e ativar o venv: python -m venv ./venv;  
3° venv\Scripts\activate;
4° Instalar dependências: pip install -r requirements.txt, django e dotenv;
5° Criar o banco: python manage.py migrate
6° Rodar: python manage.py runserver
