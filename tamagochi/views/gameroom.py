from django.shortcuts import render, redirect, reverse
from tamagochi.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def gameRoom(request):
    try:
        pet_self = Tamagochi.objects.get(user=request.user)
        new_room=Gameroom(owner=pet_self)
        new_room.save()
        pet_self.current_game_room_id = new_room.id
        pet_self.save()
        Gamerecord.objects.create(room=new_room, player=pet_self)
        return redirect(reverse('guest_gameRoom'))
    except:
        raise Http404


@login_required
def guest_gameRoom(request):
    pet_self = Tamagochi.objects.get(user=request.user)
    try:
        room=Gameroom.objects.get(id=pet_self.current_game_room_id)
    except:
        return redirect(reverse('multiIns'))
    pet_invitation_list=pet_self.play_innvitation.all()
    guests = Tamagochi.objects.filter(current_game_room_id = pet_self.current_game_room_id)
    return render(request, 'game/gameroom.html', {'room':room, 'pet':pet_self,'pet_invitation_list':pet_invitation_list, 'user':request.user, 'guests': guests})


@login_required
def get_player(request):
    try:
        user = User.objects.get(id=request.GET['user_id'])
        player = Tamagochi.objects.get(user=user)
        response = {'success': player.html8()}
        return JsonResponse(response)
    except Exception as e:
        print(e)
        raise Http404


@login_required
def get_online_friends(request):
    try:
        pet = Tamagochi.objects.get(user=request.user)
        friends_online=pet.friends.filter(online=True)
        context = {"friends":friends_online}
        return render(request, 'friends-online.json', context, content_type='application/json')
    except:
        raise Http404


@login_required
def invite_friend_play(request):
    if not 'friend_id' in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self = Tamagochi.objects.get(user=request.user)
        # invite friend=put yourself on your friend's waitlist
        pet_friend.play_innvitation.add(pet_self)
        pet_friend.save()
        return HttpResponse("")


# pop out messages only when room owner(invitation sender) is online
@login_required
def get_message(request):
    try:
        pet = Tamagochi.objects.get(user=request.user)
        play_innvitation_friends=pet.play_innvitation.filter(online=True)
        context = {"friends":play_innvitation_friends}
        return render(request, 'friends-invited.json', context, content_type='application/json')
    except:
        Http404


@login_required
def dismiss_invitation(request):
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self=Tamagochi.objects.get(user=request.user)
        # dismiss friend=remove yourself from your friend's waitlist
        pet_self.play_innvitation.remove(pet_friend)
        pet_self.save()
        print('dismissed invitation')
        return redirect(reverse("multiIns"))


@login_required
def join_room(request):
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self=Tamagochi.objects.get(user=request.user)
        room_id=pet_friend.current_game_room_id
        pet_self.play_innvitation.remove(pet_friend)
        try:
            room = Gameroom.objects.get(id=room_id)
        except:
            return redirect(reverse('multiIns'))
        if len(room.guests.all()) > 2:
            return JsonResponse({'message': 'Sorry! This room is full. '})
        if not room.room_active: 
            return JsonResponse({'message': 'Sorry! This room is inactive. '})
        room.guests.add(pet_self)
        room.save()
        pet_self.current_game_room_id=room_id
        pet_self.save()
        Gamerecord.objects.create(room=room, player=pet_self)
        print('join room',room.id,pet_self.name)
        return JsonResponse({'message':''})
