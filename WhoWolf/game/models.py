from django.db import models
from django.utils.crypto import get_random_string


class Lobby(models.Model):
    game_id = models.CharField(max_length=6, blank=True)
    host = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='lobby_host', null=True)

    @classmethod
    def create(cls):
        while True:
            game_id = get_random_string(6).upper()

            if not Lobby.objects.filter(game_id=game_id).count() > 0:
                break

        return cls(game_id=game_id)


class Player(models.Model):
    username = models.CharField(max_length=32)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='players')

    @classmethod
    def create(cls, username, lobby):
        return cls(username=username, lobby=lobby)
