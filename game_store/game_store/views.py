from django.shortcuts import render, get_object_or_404
from game_store.models import Game
from django.http import HttpResponse

def home(request):
    return render(request, "game_store/index.html")

def sign_in(request):
    return render(request, "game_store/signin.html")

def sign_up(request):
    return render(request, "game_store/signup.html")


def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        "game": game
    }
    return render(request, "game_store/game.html", context)
