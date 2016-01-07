from django.contrib import admin

from game_store.models import Game, PlayerGame, ScoreBoard

admin.site.register(Game)
admin.site.register(PlayerGame)
admin.site.register(ScoreBoard)
