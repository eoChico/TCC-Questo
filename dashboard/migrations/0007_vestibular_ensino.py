# Generated by Django 5.0.4 on 2024-04-23 01:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_nivel'),
    ]

    operations = [
        migrations.AddField(
            model_name='vestibular',
            name='ensino',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='dashboard.nivel'),
            preserve_default=False,
        ),
    ]
