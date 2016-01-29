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

def activate(request):
    if request.GET.get('user') is not None and request.GET.get('activation_key') is not None:
        user = get_object_or_404(User, id=request.GET.get('user'))
        user_profile =  get_object_or_404(User, user=user)
        if (user_profile.activation_key == request.GET.get('activation_key')):
            context = {'activated': True, 'user': user}
            user.is_activated = True
            user.save()
        else:
            context = {'error': True, 'text': "Wrong activation key"}
            
    elif request.GET.get('user') is not None and request.GET.get('activation_key') is None:
        context = {'activated': False, 'user': get_object_or_404(User, id=request.GET.get('user'))}
    else:
        context = {'error': True, 'text': "Bad request"}
    
    render(request, "game_store/activate.html", context)


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
			user.is_active=False
			user.set_password(user.password)
			
            #creating an activation key. MD5(Email + Salt).
			md5strinput = user.email + settings.SALT
			user.activation_key = md5(md5strinput.encode("ascii")).hexdigest();
		    
			user.save()
			print("Activation Url - " + settings.BASE_URL + "/activate?user=" + user.id + "&activation_key=" + user.activation_key)
			registered=True
			userprofile.save()
			

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
