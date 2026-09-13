from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import GameResult

import json

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

class RankingAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="alice",
            password="password",
        )
        self.user2 = User.objects.create_user(
            username="bob",
            password="password",
        )
        self.user3 = User.objects.create_user(
            username="charlie",
            password="password",
        )

    def test_ranking_returns_top_five_scores(self):
        scores = [
            (self.user1, 100),
            (self.user2, 500),
            (self.user3, 300),
        ]

        for user, score in scores:
            GameResult.objects.create(
                user=user,
                level=1,
                score=score,
            )

        response = self.client.get("/api/ranking/1/")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["score"], 500)
        self.assertEqual(data[1]["score"], 300)
        self.assertEqual(data[2]["score"], 100)

    def test_ranking_is_limited_to_top_five(self):
        for i in range(7):
            user = User.objects.create_user(
                username=f"user{i}",
                password="password",
            )

            GameResult.objects.create(
                user=user,
                level=1,
                score=100 + i,
            )

        response = self.client.get("/api/ranking/1/")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]["score"], 106)
        self.assertEqual(data[4]["score"], 102)

    def test_ranking_returns_only_selected_level(self):
        GameResult.objects.create(
            user=self.user1,
            level=1,
            score=500,
        )
        GameResult.objects.create(
            user=self.user2,
            level=2,
            score=1000,
        )

        response = self.client.get("/api/ranking/1/")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["score"], 500)

class RankingPageTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="alice",
            password="password",
        )
        self.bob = User.objects.create_user(
            username="bob",
            password="password",
        )

    def test_ranking_page_is_sorted_by_score_descending(self):
        GameResult.objects.create(
            user=self.alice,
            level=1,
            score=300,
        )
        GameResult.objects.create(
            user=self.bob,
            level=1,
            score=500,
        )

        self.client.force_login(user=self.alice)

        response = self.client.get("/ranking/")

        self.assertEqual(response.status_code, 200)

        scores = list(response.context["scores"])

        self.assertEqual(scores[0].score, 500)
        self.assertEqual(scores[1].score, 300)

    def test_ranking_page_can_filter_by_level(self):
        GameResult.objects.create(
            user=self.alice,
            level=1,
            score=500,
        )
        GameResult.objects.create(
            user=self.bob,
            level=2,
            score=1000,
        )

        self.client.force_login(user=self.alice)

        response = self.client.get("/ranking/?level=1")

        self.assertEqual(response.status_code, 200)

        scores = list(response.context["scores"])

        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0].level, 1)

    def test_ranking_page_can_sort_by_username(self):
        GameResult.objects.create(
            user=self.alice,
            level=1,
            score=300,
        )
        GameResult.objects.create(
            user=self.bob,
            level=1,
            score=500,
        )

        self.client.force_login(user=self.alice)

        response = self.client.get("/ranking/?sort=user_asc")

        self.assertEqual(response.status_code, 200)

        scores = list(response.context["scores"])

        self.assertEqual(scores[0].user.username, "alice")
        self.assertEqual(scores[1].user.username, "bob")

    def test_ranking_page_is_limited_to_ten_results(self):
        for i in range(12):
            user = User.objects.create_user(
                username=f"user{i}",
                password="password",
            )

            GameResult.objects.create(
                user=user,
                level=1,
                score=100 + i,
            )

        self.client.force_login(user=self.alice)

        response = self.client.get("/ranking/")

        self.assertEqual(response.status_code, 200)

        scores = list(response.context["scores"])

        self.assertEqual(len(scores), 10)