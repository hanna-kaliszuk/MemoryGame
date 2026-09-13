from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required

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

@login_required
def ranking_page(request):
    sort = request.GET.get("sort", "points_desc")
    level = request.GET.get("level", "all")

    results = GameResult.objects.select_related("user")

    if level != "all":
        results = results.filter(level=level)

    sort_fields = {
        "points_asc": "score",
        "points_desc": "-score",
        "user_asc": "user__username",
        "user_desc": "-user__username",
        "date_asc": "created_at",
        "date_desc": "-created_at",
    }

    order_by = sort_fields.get(sort, "-score")

    results = results.order_by(order_by)[:10]

    return render(
        request,
        "game/ranking.html",
        {
            "scores": results,
            "current_sort": sort,
            "current_level": level,
        },
    )