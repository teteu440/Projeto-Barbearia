from django.urls import path
from barbearia.views import index, cadastro_cliente

urlpatterns = [
    path('', index),
    path('cadastro/', cadastro_cliente, name='cadastro_cliente'),
]