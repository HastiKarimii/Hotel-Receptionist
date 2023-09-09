from datetime import timedelta, datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


class Reservation(models.Model):
    class GenderTypes(models.TextChoices):
        male = 'male'
        female = 'female'

    class RoomTypes(models.TextChoices):
        single_room = 'single_room'
        double_room = 'double_room'
        three_bedroom = 'three_bedroom'
        four_bedroom = 'four_bedroom'

    first_name = models.CharField(max_length=20, name="first_name")
    last_name = models.CharField(max_length=30, name="last_name")
    email = models.EmailField(unique=True, name="email")
    phone_number = PhoneNumberField(name="phone_number")
    address = models.CharField(max_length=200, name="address")
    number = models.IntegerField(validators=[MinValueValidator(1)])
    gender = models.CharField(max_length=10, choices=GenderTypes.choices, default=GenderTypes.male)
    room_type = models.CharField(max_length=30, choices=RoomTypes.choices, default=RoomTypes.single_room)
    login_date = models.DateField(name="login_date", default=datetime.now,
                                  validators=[MinValueValidator(datetime.today().date())])
    logout_date = models.DateField(name="logout_date")
    details = models.TextField(null=True, blank=True)

    def clean(self):
        errors = {}
        if self.login_date >= self.logout_date:
            # errors['login_date'] = 'login_date must be before logout_date.'
            errors['logout_date'] = 'logout_date must be after login_date.'

        if self.logout_date - self.login_date > timedelta(days=10):
            errors['logout_date'] = 'can not reserve a room for more than 10 nights!'

        max_guests = {
            'single_room': 1,
            'double_room': 2,
            'three_bedroom': 4,
            'four_bedroom': 6
        }
        if self.number > max_guests[self.room_type]:
            errors['number'] = 'The maximum number of guests for {} is {}.'.format(self.room_type,
                                                                                   max_guests[self.room_type])

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
