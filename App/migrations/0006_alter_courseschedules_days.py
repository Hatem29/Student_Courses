# Generated by Django 5.0.4 on 2024-05-20 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_student_email_student_first_name_student_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseschedules',
            name='days',
            field=models.CharField(choices=[('sun', 'sunday'), ('mon', 'monday'), ('tue', 'tuesday'), ('wen', 'wenday'), ('thu', 'thursday'), ('fri', 'friday'), ('sat', 'satarday')], max_length=10, null=True),
        ),
    ]
