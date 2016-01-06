from django.shortcuts import render, get_object_or_404
from game_store.models import Game
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm


def home(request):
    return render(request, "game_store/index.html")

def sign_in(request):
    return render(request, "game_store/signin.html")

def sign_up(request):
	#context = RequestContext(request)
	registered = False
	# if this is a POST request we need to process the form data
	if request.method== 'POST':
		user_form =UserForm(request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save();
			registered=True
			return render(request, "game_store/signup.html")
		else:
			print (user_form.errors)
	# if a GET (or any other method) we'll create a blank form
	else:
		user_form = UserForm()

	return render(request, 'game_store/signup.html', {'user_form': user_form})

def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        "game": game
    }
    return render(request, "game_store/game.html", context)
	
