from rest_framework import serializers

from .models import GameResult


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        # username is from the session
        # created_at is set by Django
        model = GameResult
        fields = ("level", "score")