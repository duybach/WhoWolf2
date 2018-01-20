import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.utils import timezone

from .models import Lobby
from .models import Player


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

        lobby = player.lobby

        return render(request, 'game/game.html', {'player': player, 'lobby': player.lobby,
                                                  'fellow_players': lobby.players.all()})


def status(request, game_id):
    if request.method == 'GET':
        lobby = Lobby.objects.get(game_id=game_id)
        if lobby.round == 0:
            players = lobby.players.all()
            players = [{'id': player.id, 'username': player.username} for player in players]
            data = {
                'round': lobby.round,
                'players': players,
                'host': True if lobby.host.id == request.session['user_id'] else False
            }
        else:
            players = lobby.players.all()
            players = [{'id': player.id, 'username': player.username, 'role': player.role, 'alive': player.alive, 'vote_count': player.get_votes()} for player in players]

            time = int((lobby.time - timezone.now()).total_seconds())

            data = {
                'host': True if lobby.host.username == request.session['user_id'] else False,
                'players': players,
                'round': lobby.round,
                'time': time
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
        vote = Player.objects.get(id=request.POST['vote'])
        player = Player.objects.get(id=request.session['user_id'])

        player.vote = vote
        player.save()

        return HttpResponse(json.dumps(''), content_type='application/json')
