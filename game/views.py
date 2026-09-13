from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterForm
from .models import GameResult
from .serializers import GameResultSerializer

import json
import time

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

def ranking_stream(request, level):
    def event_stream():
        while True:
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

            yield f"data: {json.dumps(data)}\n\n"

            time.sleep(2)

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )

    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"

    return response

class GameResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GameResultSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)