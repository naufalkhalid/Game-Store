from django.contrib import admin

<<<<<<< HEAD
from game_store.models import Game, PlayerGame, ScoreBoard

=======
from game_store.models import UserProfile, Game, PlayerGame, ScoreBoard

admin.site.register(UserProfile)
>>>>>>> c8b34247ebdf96e6a7c5a6d53a42d8c1bdac1550
admin.site.register(Game)
admin.site.register(PlayerGame)
admin.site.register(ScoreBoard)
