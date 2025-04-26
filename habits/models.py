from django.core.exceptions import ValidationError
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}

FREQUENCY = {
    ('daily', 'Каждый день'),
    ('3 days', 'Каждые 3 дня'),
    ('weekly', 'Каждую неделю'),
}


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit', verbose_name='пользователь',
                             **NULLABLE)
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action_habit = models.CharField(max_length=255, verbose_name='действие')
    pleasant_habit = models.BooleanField(verbose_name='приятная привычка')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, related_name='related',
                                      verbose_name='связанная привычка')
    frequency = models.CharField(max_length=30, choices=FREQUENCY, default='daily',
                                 verbose_name='частота')
    reward = models.CharField(max_length=255, verbose_name='вознагрождение', **NULLABLE)
    time_to_do = models.DurationField(verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='публичность')

    def clean(self):
        if self.related_habit and not self.related_habit.pleasant_habit:
            raise ValidationError("Можно связывать только полезные с приятными привычками")

    def __str__(self):
        return f"{self.user} {self.action_habit}"
