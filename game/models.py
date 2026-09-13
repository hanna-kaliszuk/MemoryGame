from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from .constants import MAX_LEVEL

class GameResult(models.Model):
    # each result belongs to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(MAX_LEVEL)]
    )
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)