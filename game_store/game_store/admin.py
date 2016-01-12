from django.contrib import admin

from game_store.models import UserProfile, Game, PlayerGame, ScoreBoard, Payment

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(PlayerGame)
admin.site.register(ScoreBoard)
admin.site.register(Payment)
