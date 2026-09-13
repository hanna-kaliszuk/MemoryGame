from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .forms import RegisterForm

def home(request):
    return HttpResponse("Memory Game")

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