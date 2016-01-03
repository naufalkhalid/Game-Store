from django.shortcuts import render

def home(request):
    return render(request, "game_store/index.html")
    
def sign_in(request):
    return render(request, "game_store/signin.html")
    
def sign_up(request):
    return render(request, "game_store/signup.html")
    

def game(request):
    return render(request, "game_store/game.html")