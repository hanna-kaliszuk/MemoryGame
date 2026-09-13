from rest_framework import serializers

from .constants import MAX_SCORES
from .models import GameResult


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        # username is from the session
        # created_at is set by Django
        model = GameResult
        fields = ("level", "score")

    def validate(self, attrs):
        level = attrs["level"]
        score = attrs["score"]

        if score < 0:
            raise serializers.ValidationError(
                {"score": "Score cannot be negative."}
            )

        if score > MAX_SCORES[level]:
            raise serializers.ValidationError(
                {"score": "Score is too high for this level."}
            )

        return attrs