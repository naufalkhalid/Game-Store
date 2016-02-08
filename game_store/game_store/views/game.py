from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from game_store.models import UserProfile, Game, PlayerGame, ScoreBoard, Payment
from game_store.forms import UserForm, UserProfileForm, LoginForm, GameForm, PaymentForm,EditGameForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from hashlib import md5





@login_required
def edit_game(request,game_id):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        instance = get_object_or_404(Game, id=game_id)
        
        developer=False

        if user_profile.is_developer and instance.user==user_profile.user:
                developer=True
                
        if request.method == 'GET':
            if (request.GET.get('game', False)):
                Game.objects.filter(id=game_id).delete()
                return HttpResponse("The game has been successfully deleted")
            else:    
                        #developer_form = EditGameForm()
                context = {
                    'game': instance,
                    'developer':developer
                        
                                }
                        
        elif request.method== 'POST':
                        
            developer_form=EditGameForm(request.POST or None, instance=instance)
            if developer_form.is_valid():
                                
                dev = developer_form.save(commit=False)
                    #dev.user=user_profile.user
                                
                dev.save()
                                
                context = {
                    'game': instance,
                    'developer':developer
                          }
                                
                                

            else:
                print (developer_form.errors)
                
                  

        else:
                developer=False
                context = {
                        
                        'developer':developer
                        
                        }
                
                
        return render(request, 'game_store/edit_game.html',context)	
		
#edit game here
#check if the game by same developer
	



@login_required
def add_game(request):
	developer=False
	gameadded=False
	user_profile = get_object_or_404(UserProfile, user=request.user)
	if user_profile.is_developer:
		developer=True;
	if request.method== 'POST':
		developer_form=GameForm(request.POST)
		if developer_form.is_valid():
			
			dev = developer_form.save(commit=False)
			dev.user=user_profile.user
			
			dev.save()
			gameid=dev.id;
			gameadded=True
			

		else:
			print (developer_form.errors)

    #insert code to add new game by a developer.
	else:
		developer_form = GameForm()
		gameid=""
    #check if user is a developer or not, then only allow
	return render(request, 'game_store/add_game.html', {'developer_form': developer_form,'developer':developer,'gameadded':gameadded,'gameid':gameid})


def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        "game": game,
        "game_is_purchased": False
    }
    if (request.user.is_authenticated()):
        if (PlayerGame.objects.filter(game=game, user=request.user).count() == 1):  #check if game exists in player purchases
            context['game_is_purchased'] = True

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
