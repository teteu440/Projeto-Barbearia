from django.urls import path
from barbearia.views import (
    index,
    cadastro_cliente, cadastro_barbeiro, cadastro_servico,
    listar_clientes, listar_barbeiros, listar_servicos,
)

urlpatterns = [
    path('', index),
    path('cadastro/', cadastro_cliente, name='cadastro_cliente'),
    path('cadastro/barbeiro/', cadastro_barbeiro, name='cadastro_barbeiro'),
    path('cadastro/servico/', cadastro_servico, name='cadastro_servico'),
    path('clientes/', listar_clientes, name='listar_clientes'),
    path('barbeiros/', listar_barbeiros, name='listar_barbeiros'),
    path('servicos/', listar_servicos, name='listar_servicos'),
]