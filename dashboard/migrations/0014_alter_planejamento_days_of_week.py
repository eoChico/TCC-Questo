# Generated by Django 5.0.4 on 2024-05-03 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_planejamento_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planejamento',
            name='days_of_week',
            field=models.ManyToManyField(blank=True, to='dashboard.dayofweek'),
        ),
    ]
