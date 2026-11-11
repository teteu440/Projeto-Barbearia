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
                ('data', models.DateField(verbose_name='Data')),
                ('horario', models.TimeField(verbose_name='Horário')),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('status', models.CharField(choices=[('agendado', 'Agendado'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')], default='agendado', max_length=10, verbose_name='Status')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Agendado em')),
                ('barbeiro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agendamentos', to='barbearia.barbeiro', verbose_name='Barbeiro')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agendamentos', to='barbearia.cliente', verbose_name='Cliente')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agendamentos', to='barbearia.servico', verbose_name='Serviço')),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
                'ordering': ['data', 'horario'],
            },
        ),
    ]
