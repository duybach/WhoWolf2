import random

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class Lobby(models.Model):
    game_id = models.CharField(max_length=6, blank=True)
    host = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='lobby_host', null=True)
    round = models.IntegerField(default=0)
    winning_team = models.IntegerField(default=0)
    time = models.DateTimeField(null=True)

    def assign_roles(self):
        players = self.players.all()
        for player in players:
            player.role = random.randrange(3)
            if player.role == 2:
                player.heal = 1
            player.save()

    @classmethod
    def create(cls):
        while True:
            game_id = get_random_string(6).upper()

            if not Lobby.objects.filter(game_id=game_id).count() > 0:
                break

        return cls(game_id=game_id)

    def check_winning_condition(self):
        """
        0 == Ongoing game
        1 == Team good guys won
        2 == Team bad guys won
        """
        team_1_count = 0
        team_2_count = 0
        for player in self.players.all():
            if player.alive:
                if player.role == 0:
                    team_1_count += 1
                elif player.role == 1:
                    team_2_count += 1

            if team_1_count > 0 and team_2_count > 0:
                return

        if team_1_count == 0:
            self.round = -1
            self.winning_team = 1
            self.save()

        if team_2_count == 0:
            self.round = -1
            self.winning_team = 2
            self.save()

    def set_round(self, round):
        if round == 1:
            self.round = 1
            self.time = timezone.now() + timezone.timedelta(seconds=10)
            self.save()
            self.assign_roles()

    def next_round(self):
        if self.round >= 0:
            self.round += 1
            self.time = timezone.now() + timezone.timedelta(seconds=10)
            self.save()

            for player in self.players.all():
                if self.round % 2 == 1:
                    if player.voters.count() > self.players.count()/2:
                        player.alive = False
                elif self.round % 2 == 0:
                    if player.killers.count() > 0:
                        if not player.healers.count() > 0:
                            player.alive = False

                    if player.heal_target:
                        player.heal -= 1

                player.save()

            for player in self.players.all():
                player.reset_actions()

        self.check_winning_condition()


class Player(models.Model):
    username = models.CharField(max_length=32)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='players')
    alive = models.BooleanField(default=True)
    role = models.IntegerField(default=0)
    heal = models.IntegerField(default=0)
    vote_target = models.ForeignKey('self', default=None, null=True, on_delete=models.SET_NULL, related_name='voters')
    kill_target = models.ForeignKey('self', default=None, null=True, on_delete=models.SET_NULL, related_name='killers')
    heal_target = models.ForeignKey('self', default=None, null=True, on_delete=models.SET_NULL, related_name='healers')

    @classmethod
    def create(cls, username, lobby):
        return cls(username=username, lobby=lobby)

    def reset_actions(self):
        self.vote_target = None
        self.kill_target = None
        self.heal_target = None
        self.save()
