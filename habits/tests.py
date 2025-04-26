from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user(
            username='Test',
            password='test'
        )
        self.client.force_authenticate(user=self.user)

        self.habit1 = Habit.objects.create(
            user=self.user,
            place="test",
            time="10:00:00",
            action_habit="test1",
            pleasant_habit=False,
            frequency="daily",
            reward=None,
            time_to_do="00:02:00",
            is_public=False
        )

        self.habit2 = Habit.objects.create(
            user=self.user,
            place="test",
            time="10:00:00",
            action_habit="test2",
            pleasant_habit=True,
            frequency="daily",
            reward=None,
            time_to_do="00:01:00",
            is_public=True
        )

    def test_habit_list(self):
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['action'], "test2")

    def test_HabitCreate(self):
        data = {
            "place": "test",
            "time": "10:00:00",
            "action_habit": "test3",
            "pleasant_habit": False,
            "frequency": "day",
            "reward": "test",
            "time_to_do": "00:01:00",
            "is_public": True
        }
        response = self.client.post('/habits/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.filter(action="Meditate").first()
        self.assertIsNotNone(habit)
        self.assertEqual(habit.user, self.user)

    def test_HabitCreate_validation(self):
        invalid1 = {
            "place": "test",
            "time": "10:00:00",
            "action_habit": "test",
            "pleasant_habit": False,
            "related_habit": self.habit2.id,
            "frequency": "day",
            "reward": "test",
            "time_to_do": "00:02:10",
            "is_public": True
        }
        invalid2 = {
            "place": "test",
            "time": "10:00:00",
            "action_habit": "test",
            "pleasant_habit": False,
            "related_habit": self.habit1.id,
            "frequency": "day",
            "reward": "00:02:00",
            "is_public": True
        }
        response = self.client.post('/habits/create/', invalid1)
        response2 = self.client.post('/habits/create/', invalid2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.json()
        errors2 = response2.json()
        self.assertIn("Время выполнения не должно превышать 0:02:00.", errors["non_field_errors"])
        self.assertIn("Разрешёно только выбрать связанную привычку или вознаграждение", errors["non_field_errors"])
        self.assertIn("Можно связывать только полезные с приятными привычками", errors2["non_field_errors"])

    def test_HabitUpdate(self):
        updated_data = {
            "place": "test_updated",
            "time": "11:00:00",
            "action_habit": "test_updated",
            "pleasant_habit": True,
            "frequency": "3 days",
            "reward": '',
            "time_to_do": "00:01:00",
            "is_public": False
        }
        response = self.client.put(f'/habits/update/{self.habit1.id}', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        habit = Habit.objects.get(id=self.habit1.id)
        self.assertEqual(habit.place, "test_updated")
        self.assertEqual(habit.action_habit, "test_updated")

    def test_HabitDestroy(self):
        response = self.client.delete(f'/habits/delete/{self.habit1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_HabitDetail(self):
        response = self.client.get(f'/habits/detail/{self.habit2.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['action_habit'], "test2")
        self.assertEqual(data['is_public'], True)