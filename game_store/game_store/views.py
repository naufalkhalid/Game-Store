from django.shortcuts import render, get_object_or_404
from game_store.models import Game, PlayerGame, ScoreBoard
from game_store.forms import UserForm, UserProfileForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, "game_store/index.html")


def sign_in(request):
    if (request.user.is_authenticated()):
        return HttpResponseRedirect('/')

    login_form = LoginForm(request.POST or None)
    if (request.method == 'POST'):
        if (login_form.is_valid()): #this will also authenticate the user
            login_form.login(request)
            return HttpResponseRedirect('/')

    return render(request, "game_store/signin.html", {'form': login_form})


def sign_up(request):
    if (request.method == 'GET'):
        return render(request, "game_store/signup.html")
    elif (request.method == 'POST'):
        pass


def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        "game": game
    }
    return render(request, "game_store/game.html", context)


"""
Function Name: score
Description: This function adds an entry to the scoreboard table. The user needs to be logged in for this operation.
Post data:
    Game_Id: The Game to which the score is added
    Score: The score which needs to be submitted
Returns: 200 OK if successful, 401 if unauthorized, 404 if game not found.
"""
def score(request):
    #TODO - check if user is logged in, get his user id
    if (request.method == 'POST'):
        if ((request.POST['game'] is not None) and (request.POST['score'] is not None)):
            try:
                user = User.objects.get(id=1) #HARD CODED for NOW
                game = Game.objects.get(id=request.POST['game'])
                score_value = request.POST['score']
                if (PlayerGame.objects.filter(game=game, user=user).count() == 1):  #check if game exists in player purchases
                    scoreboard = ScoreBoard(game=game, user=user, score=score_value) #create new ScoreBoard entry and save
                    scoreboard.save()
                    return HttpResponse("OK", status=200)
                else:
                    return HttpResponse("GAME PURCHASE NOT FOUND", status=404)
            except Game.DoesNotExist:
                return HttpResponse("GAME/USER NOT FOUND", status=404)
    else:
        return HttpResponse("METHOD NOT ALLOWED", status=405)
