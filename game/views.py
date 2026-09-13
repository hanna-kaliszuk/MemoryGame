from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterForm
from .models import GameResult
from .serializers import GameResultSerializer

def home(request):
    return render(request, "game/game.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

def ranking(request, level):
    results = (
        GameResult.objects
        .filter(level=level)
        .select_related("user")
        .order_by("-score", "user__username")[:5]
    )

    data = [
        {
            "username": result.user.username,
            "score": result.score,
        }
        for result in results
    ]

    return JsonResponse(data, safe=False)

class GameResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GameResultSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)