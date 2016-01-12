from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from game_store.models import UserProfile, Game, PlayerGame, ScoreBoard, Payment
from game_store.forms import UserForm, UserProfileForm, LoginForm, GameForm, PaymentForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

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
