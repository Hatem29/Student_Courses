# Generated by Django 5.0.4 on 2024-05-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_remove_courses_scheduled_courseschedules_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentreg',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]