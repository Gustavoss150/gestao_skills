# Generated by Django 5.1.1 on 2024-11-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_treinamento_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='treinamento',
            name='nome',
            field=models.CharField(default='Desconhecido', max_length=100),
        ),
    ]