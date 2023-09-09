# Generated by Django 4.2.5 on 2023-09-09 13:03

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10)),
                ('room_type', models.CharField(choices=[('single_room', 'Single Room'), ('double_room', 'Double Room'), ('three_bedroom', 'Three Bedroom'), ('four_bedroom', 'Four Bedroom')], default='single_room', max_length=30)),
                ('login_date', models.DateField()),
                ('logout_date', models.DateField()),
                ('details', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
