# Generated by Django 5.2 on 2025-04-29 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuhk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='reservation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cuhk.reservation'),
        ),
    ]
