# Generated by Django 5.0.6 on 2024-05-29 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_remove_courses_prerequisites_courses_prerequisites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseschedules',
            name='course',
        ),
        migrations.AddField(
            model_name='courses',
            name='courseSchedules',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.courseschedules'),
        ),
    ]
