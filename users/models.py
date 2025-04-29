from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.CharField(verbose_name='id чата телеграма')

    REQUIRED_FIELDS = ['email', 'telegram_id']

    def __str__(self):
        return self.username
