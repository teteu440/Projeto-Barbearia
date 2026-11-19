from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    # Autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/novo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente_delete'),

    # Barbeiros
    path('barbeiros/', views.BarbeiroListView.as_view(), name='barbeiro_list'),
    path('barbeiros/novo/', views.BarbeiroCreateView.as_view(), name='barbeiro_create'),
    path('barbeiros/<int:pk>/editar/', views.BarbeiroUpdateView.as_view(), name='barbeiro_update'),
    path('barbeiros/<int:pk>/excluir/', views.BarbeiroDeleteView.as_view(), name='barbeiro_delete'),

    # Serviços
    path('servicos/', views.ServicoListView.as_view(), name='servico_list'),
    path('servicos/novo/', views.ServicoCreateView.as_view(), name='servico_create'),
    path('servicos/<int:pk>/editar/', views.ServicoUpdateView.as_view(), name='servico_update'),
    path('servicos/<int:pk>/excluir/', views.ServicoDeleteView.as_view(), name='servico_delete'),

    # Agenda
    path('agenda/', views.AgendaView.as_view(), name='agendamento_list'),
    path('agenda/novo/', views.AgendamentoCreateView.as_view(), name='agendamento_create'),
    path('agenda/<int:pk>/editar/', views.AgendamentoUpdateView.as_view(), name='agendamento_update'),
    path('agenda/<int:pk>/excluir/', views.AgendamentoDeleteView.as_view(), name='agendamento_delete'),
    path('agenda/<int:pk>/avisar/', views.AgendamentoComunicarView.as_view(), name='agendamento_comunicar'),
    path('agenda/<int:pk>/status/<str:status>/', views.AgendamentoStatusView.as_view(), name='agendamento_status'),
]
