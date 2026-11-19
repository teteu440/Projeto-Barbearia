import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbearia', '0002_barbeiro_servico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField(verbose_name='Início')),
                ('fim', models.DateTimeField(editable=False, verbose_name='Término')),
                ('preco', models.DecimalField(decimal_places=2, editable=False, max_digits=8, null=True, verbose_name='Valor (R$)')),
                ('status', models.CharField(choices=[('agendado', 'Agendado'), ('confirmado', 'Confirmado'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado'), ('faltou', 'Não compareceu')], default='agendado', max_length=12, verbose_name='Status')),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
                ('barbeiro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agendamentos', to='barbearia.barbeiro', verbose_name='Barbeiro')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agendamentos', to='barbearia.cliente', verbose_name='Cliente')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agendamentos', to='barbearia.servico', verbose_name='Serviço')),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
                'ordering': ['inicio'],
            },
        ),
    ]
