from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_game', views.create_game, name='create_game'),
    path('join_game', views.join_game, name='join_game'),
    path('game', views.game, name='game'),

    # ajax api
    path('game/<str:game_id>/get_players', views.get_players, name='get_players')
]
