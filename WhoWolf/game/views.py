import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.utils import timezone

from .models import Lobby
from .models import Player
from WhoWolf import settings


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
        time_per_round = request.POST.get('InputTimeNumber', 60)
        if time_per_round >= 15:
            lobby.time_per_round = time_per_round
        else:
            lobby.time_per_round = 60
        lobby.werewolf_count = request.POST.get('InputWerwolfNumber', 0)
        lobby.witch_count = request.POST.get('InputWitchNumber', 0)
        lobby.save()

        request.session['user_id'] = player.id

        return redirect('game:game')


def join_game(request):
    if request.method == 'GET':
        return render(request, 'game/join.html', {})
    elif request.method == 'POST':
        game_id = request.POST['InputCode'].upper()
        try:
            lobby = Lobby.objects.get(game_id=game_id)
        except Lobby.DoesNotExist:
            lobby = None

        if lobby:
            player = Player.create(request.POST.get('InputUserName', 'Anon'), lobby)
            player.save()

            request.session['user_id'] = player.id

            return redirect('game:game')
        else:
            context = {
                'InputUserName': request.POST.get('InputUserName', ''),
                'InputCode': request.POST.get('InputCode', ''),
                'error_message': True
            }
            return render(request, 'game/join.html', context)


def game(request):
    if request.method == 'GET':
        player = Player.objects.get(id=request.session['user_id'])
        return render(request, 'game/game.html', {'player': player, 'lobby': player.lobby})


def game_end(request):
    if request.method == 'GET':
        player = Player.objects.get(id=request.session['user_id'])
        context = {'player': player, 'lobby': player.lobby, 'players': player.lobby.players.all()}
        return render(request, 'game/game_end.html', context)


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
                    'vote_count': fellow_player.voters.count(),
                }

                if lobby.round % 2 == 0:
                    if player.vote_target and player.vote_target.id == fellow_player.id:
                        fellow_player_dict.update({'selected': True})
                elif lobby.round % 2 == 1:
                    if player.kill_target and player.kill_target.id == fellow_player.id or \
                       player.heal_target and player.heal_target.id == fellow_player.id:
                        fellow_player_dict.update({'selected': True})
                    if player.role == 1:
                        fellow_player_dict.update({'kill_count': fellow_player.killers.count()})

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

            if time <= 0:
                lobby.next_round()

        return HttpResponse(json.dumps(data), content_type='application/json')


def start(request, game_id):
    if request.method == 'POST':
        lobby = Lobby.objects.get(game_id=game_id)
        if not lobby.round >= 1:
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
