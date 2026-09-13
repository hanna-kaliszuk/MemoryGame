from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import GameResult

class GameResultAPITests(APITestCase):
    def test_unauthenticated_user_cannot_submit_result(self):
        response = self.client.post(
            "/api/results/",
            {"level": 1, "score": 500},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_submit_result(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/results/",
            {"level": 1, "score": 500},
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(GameResult.objects.count(), 1)

        result = GameResult.objects.get()

        self.assertEqual(result.user, user)
        self.assertEqual(result.level, 1)
        self.assertEqual(result.score, 500)



