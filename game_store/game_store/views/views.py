from django.shortcuts import render, get_object_or_404
from game_store.models import UserProfile, Game, PlayerGame
from django.contrib.auth.decorators import login_required

def home(request):
    games = Game.objects.all()
    return render(request, "game_store/index.html", {'games': games})

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
