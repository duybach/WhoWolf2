import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse

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

        request.session['InputUserName'] = player.username

        return redirect('game:game')


def join_game(request):
    if request.method == 'GET':
        return render(request, 'game/join.html', {})
    elif request.method == 'POST':
        game_id = request.POST['InputCode'].upper()
        lobby = Lobby.objects.get(game_id=game_id)

        player = Player.create(request.POST['InputUserName'], lobby)
        player.save()

        request.session['InputUserName'] = player.username

        return redirect('game:game')


def game(request):
    if request.method == 'GET':
        player = Player.objects.get(username=request.session['InputUserName'])

        lobby = player.lobby

        return render(request, 'game/game.html', {'player': player, 'lobby': player.lobby,
                                                  'fellow_players': lobby.players.all()})


def get_players(request, game_id):
    lobby = Lobby.objects.get(game_id=game_id)
    players = lobby.players.all()
    data = [{'username': player.username} for player in players]
    return HttpResponse(json.dumps(data), content_type="application/json")
