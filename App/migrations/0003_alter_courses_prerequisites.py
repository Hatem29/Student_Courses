# Generated by Django 5.0.4 on 2024-05-14 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_courses_prerequisites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='prerequisites',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='App.courses'),
        ),
    ]