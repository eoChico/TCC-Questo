# Generated by Django 5.0.3 on 2024-04-12 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_prova_vestibular_correcao_caderno_prova_vestibular'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correcao',
            name='prova',
        ),
        migrations.AddField(
            model_name='correcao',
            name='caderno',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='dashboard.caderno'),
            preserve_default=False,
        ),
    ]
