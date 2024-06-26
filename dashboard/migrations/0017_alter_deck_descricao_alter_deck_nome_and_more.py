# Generated by Django 5.0.4 on 2024-06-06 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_vestibular_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='descricao',
            field=models.TextField(max_length=70),
        ),
        migrations.AlterField(
            model_name='deck',
            name='nome',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='evento',
            name='titulo',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='pergunta',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='resposta',
            field=models.CharField(max_length=150),
        ),
    ]
