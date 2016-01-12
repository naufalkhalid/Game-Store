from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from game_store.models import UserProfile, Game, PlayerGame, ScoreBoard, Payment
from game_store.forms import UserForm, UserProfileForm, LoginForm, GameForm, PaymentForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from hashlib import md5


def home(request):
    return render(request, "game_store/index.html")


@login_required
def dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    #games purchased by the user
    player_games = PlayerGame.objects.filter(user=request.user)
    #games developed by the user. Since query sets are lazy, the condition will be checked in the template
    developer_games = Game.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
        'player_games': player_games,
        'developer_games': developer_games
    }
    return render(request, "game_store/dashboard.html", context)
