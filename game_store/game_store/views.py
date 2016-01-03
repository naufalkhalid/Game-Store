from django.shortcuts import render

def home(request):
    return render(request, "game_store/index.html")
    
def sign_in(request):
    return render(request, "game_store/index.html")
    
def sign_up(request):
    return render(request, "game_store/index.html")