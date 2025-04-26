from datetime import timedelta

from rest_framework import serializers


class LimitTimeToDo:
    def __init__(self):
        self.max_duration = timedelta(minutes=2)

    def __call__(self, value):
        time_to_do = value.get('time_to_do')
        if time_to_do and time_to_do > self.max_duration:
            raise serializers.ValidationError(f"Время выполнения не должно превышать {self.max_duration}.")


class ValidRelatedHabit:
    def __call__(self, value):
        new_obj = value.get('related_habit')
        if new_obj and not new_obj.pleasant_habit:
            raise serializers.ValidationError("Можно связывать только полезные с приятными привычками")


class RelatedHabitOrReward:
    def __call__(self, value):
        if value.get('related_habit') and value.get('reward'):
            raise serializers.ValidationError('Выберите либо связанную привычку либо вознаграждение')
