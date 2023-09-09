from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class Receptionist(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        unique_together = ('username', 'email',)

    def __str__(self):
        return self.username
