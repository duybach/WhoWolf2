from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_game', views.create_game, name='create_game'),
    path('join_game', views.join_game, name='join_game'),
    path('game', views.game, name='game'),
    path('game_end', views.game_end, name='game_end'),
    path('blubb', views.blubb, name='blubb'),

    # ajax api
    path('game/<str:game_id>/status', views.status, name='status'),
    path('game/<str:game_id>/start', views.start, name='start'),
    path('game/<str:game_id>/vote', views.vote, name='vote'),
    path('game/<str:game_id>/kill', views.kill, name='kill'),
    path('game/<str:game_id>/heal', views.heal, name='heal')
]
