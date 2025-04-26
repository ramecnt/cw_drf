from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitCreateAPIView, HabitUpdateAPIView, HabitDestroyAPIView, \
    HabitDetailAPIView, HabitOwnListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('list/', HabitListAPIView.as_view(), name='habit_list'),
    path('list/own/', HabitOwnListAPIView.as_view(), name='habit_own_list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('detail/<int:pk>', HabitDetailAPIView.as_view(), name='habit_detail'),
    path('delete/<int:pk>', HabitDestroyAPIView.as_view(), name='habit_delete'),
    path('update/<int:pk>', HabitUpdateAPIView.as_view(), name='habit_update'),
]
