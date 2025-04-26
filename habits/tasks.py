from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from habits.models import Habit
from habits.services import send_tg_message, is_today


@shared_task
def habit_remind():
    date = now().date()
    time = now().time()

    for habit in Habit.objects.all():
        habit_time = timedelta(
            hours=habit.time.hour,
            minutes=habit.time.minute,
            seconds=habit.time.second
        ).total_seconds()

        current_time = timedelta(
            hours=time.hour,
            minutes=time.minute,
            seconds=time.second
        ).total_seconds()

        if abs(habit_time - current_time) < 60:
            if is_today(habit.frequency, habit.user.date_joined.date(), date) and habit.user.telegram_id:
                send_tg_message(habit.user.telegram_id,
                                f"Пора выполнить привычку '{habit.action_habit}' в {habit.place}.")
