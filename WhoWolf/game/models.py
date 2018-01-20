import random

from django.db import models
from django.utils.crypto import get_random_string

from WhoWolf.settings import GAME_ROLES


class Lobby(models.Model):
    game_id = models.CharField(max_length=6, blank=True)
    host = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='lobby_host', null=True)
    round = models.IntegerField(default=0)
    time = models.IntegerField(default=60)
    night = models.BooleanField(default=True)

    def assign_roles(self):
        print('assigning roles ...')
        players = self.players.all()
        for player in players:
            player.role = random.choice(GAME_ROLES)
            player.save()

    @classmethod
    def create(cls):
        while True:
            game_id = get_random_string(6).upper()

            if not Lobby.objects.filter(game_id=game_id).count() > 0:
                break

        return cls(game_id=game_id)

    def set_round(self, round):
        if round == 1:
            self.round = 1
            self.save()
            self.assign_roles()


class Player(models.Model):
    username = models.CharField(max_length=32)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='players')
    role = models.CharField(max_length=32, blank=True)
    alive = models.BooleanField(default=True)

    @classmethod
    def create(cls, username, lobby):
        return cls(username=username, lobby=lobby)
