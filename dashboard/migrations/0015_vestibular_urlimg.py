# Generated by Django 5.0.4 on 2024-05-06 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_planejamento_days_of_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='vestibular',
            name='urlImg',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
