# Generated by Django 5.0.4 on 2024-04-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_rename_diasemana_dayofweek_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='planejamento',
            name='hora',
            field=models.TimeField(default='10:00'),
            preserve_default=False,
        ),
    ]
