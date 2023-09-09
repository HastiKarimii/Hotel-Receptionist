# Generated by Django 4.2.5 on 2023-09-09 14:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_alter_reservation_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='number',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]