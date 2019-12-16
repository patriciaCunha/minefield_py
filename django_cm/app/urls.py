from django.conf.urls import include
from app.views import play_game, start_game

from django.urls import path
urlpatterns = [
    path('start/', start_game, name='init_game'),
    path('game/<int:pk>', play_game, name='play_game'),
]
