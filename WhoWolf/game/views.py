import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.utils import timezone

from .models import Lobby
from .models import Player
from WhoWolf import settings


# Create your views here.
def index(request):
    return render(request, 'game/index.html', {})


def create_game(request):
    if request.method == 'GET':
        return render(request, 'game/create.html', {})
    if request.method == 'POST':
        lobby = Lobby.create()
        lobby.save()

        player = Player.create(request.POST['InputUserName'], lobby)
        player.save()

        lobby.host = player
        lobby.save()

        request.session['user_id'] = player.id

        return redirect('game:game')


def join_game(request):
    if request.method == 'GET':
        return render(request, 'game/join.html', {})
    elif request.method == 'POST':
        game_id = request.POST['InputCode'].upper()
        lobby = Lobby.objects.get(game_id=game_id)

        player = Player.create(request.POST['InputUserName'], lobby)
        player.save()

        request.session['user_id'] = player.id

        return redirect('game:game')


def game(request):
    if request.method == 'GET':
        player = Player.objects.get(id=request.session['user_id'])
        return render(request, 'game/game.html', {'player': player, 'lobby': player.lobby})


def game_end(request):
    if request.method == 'GET':
        player = Player.objects.get(id=request.session['user_id'])
        return render(request, 'game/game_end.html', {'player': player, 'lobby': player.lobby, 'players': player.lobby.players.all()})


def status(request, game_id):
    player = Player.objects.get(id=request.session['user_id'])

    if request.method == 'GET':
        lobby = Lobby.objects.get(game_id=game_id)
        if lobby.round == 0:
            players = []
            for fellow_player in lobby.players.all():
                players.append({
                    'id': fellow_player.id,
                    'username': fellow_player.username
                })
            data = {
                'round': lobby.round,
                'players': players,
                'host': True if lobby.host.id == request.session['user_id'] else False
            }
        elif lobby.round == -1:
            players = []
            for fellow_player in lobby.players.all():
                players.append({
                    'id': fellow_player.id,
                    'username': fellow_player.username
                })
            data = {
                'winning_team': lobby.winning_team,
                'players': players,
                'host': True if lobby.host.id == request.session['user_id'] else False
            }
        else:
            players = []
            for fellow_player in lobby.players.all():
                fellow_player_dict = {
                    'id': fellow_player.id,
                    'username': fellow_player.username,
                    'alive': fellow_player.alive,
                    'vote_count': fellow_player.voters.count()
                }

                if player.vote_target and player.vote_target.id == fellow_player.id or \
                   player.kill_target and player.kill_target.id == fellow_player.id or \
                   player.heal_target and player.heal_target.id == fellow_player.id:
                    fellow_player_dict.update({'selected': True})

                players.append(fellow_player_dict)

            time = int((lobby.time - timezone.now()).total_seconds())

            role = {'id': player.role, 'name': settings.ROLES[player.role]}

            if role['id'] == 2:
                role.update({'heal': player.heal})

            data = {
                'id': player.id,
                'alive': player.alive,
                'role': role,
                'players': players,
                'round': lobby.round,
                'time': time,
                'host': True if lobby.host.username == request.session['user_id'] else False
            }

            if lobby.round % 2 == 1:
                # night time
                pass
            elif lobby.round % 2 == 0:
                # day time
                pass

            if time <= 0:
                lobby.next_round()

        print(data)

        return HttpResponse(json.dumps(data), content_type='application/json')


def start(request, game_id):
    if request.method == 'POST':
        lobby = Lobby.objects.get(game_id=game_id)
        lobby.set_round(1)

        return HttpResponse(json.dumps(''), content_type='application/json')


def vote(request, game_id):
    if request.method == 'POST':
        vote_target = Player.objects.get(id=request.POST['vote_target'])
        player = Player.objects.get(id=request.session['user_id'])

        player.vote_target = vote_target
        player.save()

        return HttpResponse(json.dumps(''), content_type='application/json')


def kill(request, game_id):
    if request.method == 'POST':
        kill_target = Player.objects.get(id=request.POST['kill_target'])
        player = Player.objects.get(id=request.session['user_id'])

        player.kill_target = kill_target
        player.save()

        return HttpResponse(json.dumps(''), content_type='application/json')


def heal(request, game_id):
    if request.method == 'POST':
        heal_target = Player.objects.get(id=request.POST['heal_target'])
        player = Player.objects.get(id=request.session['user_id'])

        if player.heal > 0:
            player.heal_target = heal_target
            player.save()

        return HttpResponse(json.dumps(''), content_type='application/json')
