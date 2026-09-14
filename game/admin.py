from django.contrib import admin

from .models import GameResult

@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "score", "created_at")
    list_filter = ("level",)
    search_fields = ("user__username",)
    ordering = ("-score",)