from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.register, name="register"),
    path("api/results/", views.GameResultView.as_view(), name="game-results"),
    path("api/ranking/<int:level>/", views.ranking, name="ranking"),
]