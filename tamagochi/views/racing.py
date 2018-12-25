from django.shortcuts import render
from tamagochi.models import *
from django.template.defaultfilters import register
from django.contrib.auth.decorators import login_required
from django.http import Http404


@register.filter
def keyValue(dic, key):
    return dic[key]


@login_required
def racingGame(request):
    try:
        pet = Tamagochi.objects.get(user=request.user)
        number = pet.current_game_room_id
        players = Tamagochi.objects.filter(current_game_room_id=number)
        room = Gameroom.objects.get(id=number)
        records = {record.player: record.score for record in Gamerecord.objects.filter(room=room, score__isnull=False)}
        return render(request, 'game/racinggame.html', {'room':room, 'pet':pet, 'user': request.user, 'players': players, 'records': records})
    except:
        raise Http404
