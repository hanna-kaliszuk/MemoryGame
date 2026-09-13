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

    def test_invalid_level_is_rejected(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/results/",
            {"level": 5, "score": 500},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_score_is_rejected(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/results/",
            {"level": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_level_is_rejected(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/results/",
            {"score": 500},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_result_is_assigned_to_authenticated_user(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        self.client.post(
            "/api/results/",
            {"level": 2, "score": 750},
            format="json",
        )

        result = GameResult.objects.get()

        self.assertEqual(result.user, user)

    def test_negative_score_is_rejected(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/results/",
            {"level": 1, "score": -1},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(GameResult.objects.count(), 0)


    def test_score_above_level_maximum_is_rejected(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/results/",
            {"level": 1, "score": 1401},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(GameResult.objects.count(), 0)


    def test_maximum_valid_score_is_accepted(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/results/",
            {"level": 1, "score": 1400},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(GameResult.objects.count(), 1)

        result = GameResult.objects.get()

        self.assertEqual(result.user, user)
        self.assertEqual(result.level, 1)
        self.assertEqual(result.score, 1400)
