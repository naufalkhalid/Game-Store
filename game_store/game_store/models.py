from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #developer
    title = models.CharField(max_length=250)
    href = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=250)

class PlayerGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_on = models.DateTimeField(auto_now_add=True)
    purchased_price = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=3000)

class ScoreBoard(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
