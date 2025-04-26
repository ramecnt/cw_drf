from rest_framework import serializers

from habits.models import Habit
from habits.validator import RelatedHabitOrReward, LimitTimeToDo, ValidRelatedHabit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [LimitTimeToDo(), ValidRelatedHabit(), RelatedHabitOrReward()]