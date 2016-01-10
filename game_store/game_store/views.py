from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from game_store.models import UserProfile, Game, PlayerGame, ScoreBoard
from game_store.forms import UserForm, UserProfileForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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

def add_game(request):
    #insert code to add new game by a developer.
    #check if user is a developer or not, then only allow
    pass


def sign_up(request):
	#context = RequestContext(request)
	registered = False
	# if this is a POST request we need to process the form data
	if request.method== 'POST':
		user_form =UserForm(request.POST)
		user_profile_form=UserProfileForm(request.POST)
		if user_form.is_valid() and user_profile_form.is_valid() :
			user = user_form.save()
			userprofile=user_profile_form.save(commit=False);
			userprofile.user=user
			user.set_password(user.password)

			user.save();
			userprofile.save();
			registered=True

		else:
			print (user_form.errors)
	# if a GET (or any other method) we'll create a blank form
	else:
		user_form = UserForm()
		user_profile_form=UserProfileForm()

	return render(request, 'game_store/signup.html', {'user_form': user_form, 'user_profile_form':user_profile_form, 'registered':registered})


def sign_in(request):
    if (request.GET.get('next') is not None):
        next_page = request.GET.get('next')
    else:
        next_page = '/'

    if (request.user.is_authenticated()):
        return HttpResponseRedirect(next_page)

    login_form = LoginForm(request.POST or None)
    if (request.method == 'POST'):
        if (login_form.is_valid()): #this will also authenticate the user
            login_form.login(request)
            return HttpResponseRedirect(next_page)
    return render(request, "game_store/signin.html", {'form': login_form, 'next_page': next_page})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        "game": game
    }
    if (request.user.is_authenticated()):
        if (PlayerGame.objects.filter(game=game, user=request.user).count() == 1):  #check if game exists in player purchases
            context['game_is_purchased'] = True
        else:
            context['game_is_purchased'] = False
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
    if not request.user.is_authenticated():
        return HttpResponse("Login required", status=403)
    else:
        if (request.method == 'POST'):
            if ((request.POST['game'] is not None) and (request.POST['score'] is not None)):
                try:
                    user = request.user
                    game = Game.objects.get(id=request.POST['game'])
                    score_value = request.POST['score']
                    if (PlayerGame.objects.filter(game=game, user=user).count() == 1):  #check if game exists in player purchases
                        scoreboard = ScoreBoard(game=game, user=user, score=score_value) #create new ScoreBoard entry and save
                        scoreboard.save()
                        return HttpResponse("OK", status=200)
                    else:
                        return HttpResponse("Game purchase not found", status=404)
                except Game.DoesNotExist:
                    return HttpResponse("Game not found", status=404)
        else:
            return HttpResponse("Method not allowed", status=405)

"""
Function Name: state
Description: This function replaces the "Save" field with recent data of the game.
The user needs to be logged in for this operation.
Post data:
    Game_Id: The Game to which the score is added
    state: The state which needs to be saved
Returns: 200 OK if successful, 401 if unauthorized, 404 if game not found.
"""
def state(request):
    if not request.user.is_authenticated():
        return HttpResponse("Login required", status=403)
    else:
        #if the request is POST, then save the game state
        if (request.method == 'POST'):
            if ((request.POST['game'] is not None) and (request.POST['state'] is not None)):
                try:
                    user = request.user
                    game = Game.objects.get(id=request.POST['game'])
                    state = request.POST['state']
                    playerGame = PlayerGame.objects.get(game=game, user=user)
                    playerGame.state = state
                    playerGame.save()
                    return HttpResponse("OK", status=200)
                except (PlayerGame.DoesNotExist, Game.DoesNotExist):
                    return HttpResponse("Game/Purchase not found", status=404)

        #if the request is GET, then return the game state
        elif (request.method == 'GET'):
            if (request.GET['game'] is not None):
                try:
                    user = request.user
                    game = Game.objects.get(id=request.GET['game'])
                    playerGame = PlayerGame.objects.get(game=game, user=user)
                    return HttpResponse(playerGame.state, status=200)
                except (PlayerGame.DoesNotExist, Game.DoesNotExist):
                    return HttpResponse("Game/Purchase not found", status=404)
        else:
            return HttpResponse("Method not allowed", status=405)
