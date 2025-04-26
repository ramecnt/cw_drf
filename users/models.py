from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    telegram_id = models.CharField(**NULLABLE, verbose_name='id чата телеграма')

    def __str__(self):
        return self.username
