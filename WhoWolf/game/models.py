import random

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from WhoWolf.settings import GAME_ROLES


class Lobby(models.Model):
    game_id = models.CharField(max_length=6, blank=True)
    host = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='lobby_host', null=True)
    round = models.IntegerField(default=0)
    time = models.DateTimeField(null=True)

    def assign_roles(self):
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
            self.time = timezone.now() + timezone.timedelta(seconds=10)
            self.save()
            self.assign_roles()

    def next_round(self):
        self.round += 1
        self.time = timezone.now() + timezone.timedelta(seconds=10)
        self.save()

        for player in self.players.all():
            if self.round % 2 == 1:
                if player.get_votes() > self.players.count()/2:
                    player.alive = False

                player.vote = None
                player.save()


class Player(models.Model):
    username = models.CharField(max_length=32)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='players')
    role = models.CharField(max_length=32, blank=True)
    alive = models.BooleanField(default=True)
    vote = models.ForeignKey('self', default=None, null=True, on_delete=models.SET_NULL, related_name='voters')

    @classmethod
    def create(cls, username, lobby):
        return cls(username=username, lobby=lobby)

    def get_votes(self):
        return self.voters.count()
