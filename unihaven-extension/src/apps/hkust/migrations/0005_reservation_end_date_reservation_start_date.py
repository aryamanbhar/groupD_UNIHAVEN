# Generated by Django 5.1.7 on 2025-04-29 16:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkust', '0004_rename_degree_type_student_university_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='end_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='reservation',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
