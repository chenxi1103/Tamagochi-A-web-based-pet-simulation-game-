from django.shortcuts import render
from tamagochi.models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required
def playCastle(request):
    try:
        pet_self = Tamagochi.objects.get(user=request.user)
        pet_invitation_list=pet_self.play_innvitation.all()
        return render(request, 'game/gameMode.html', {'pet_invitation_list':pet_invitation_list})
    except:
        raise Http404


@login_required
def multiIns(request):
    try:
        message=[]
        pet = Tamagochi.objects.get(user=request.user)
        ranking = Tamagochi.objects.filter(score3__gt=0).order_by('score3')[:3]
        pet_invitation_list=pet.play_innvitation.all()
        return render(request, 'game/multiIns.html', {'pet':pet, 'ranking': ranking, 'pet_invitation_list':pet_invitation_list})
    except:
        raise Http404


@login_required
def check_status(request):
    pet = Tamagochi.objects.get(user=request.user)
    pet_energy=pet.energy
    pet_health=pet.health
    pet_sickness=pet.sickness
    game_status=False
    pet_id=pet.id
    if pet_sickness == True:
        message="Sick pet cannot play games, please go to hospital to treat your pet."
    elif pet_energy < 20:
        message="Your pet's energy cannot be lower than 50 for this game."
    elif pet_health < 20:
        message = "Your pet's health cannot be lower than 50 for this game."
    else:
        message = "You pass the health/energy test, have fun!"
        game_status = 'Ready'
    context = {'message':message,'game_status':game_status,'pet_id':pet_id}
    return render(request, 'check_status.json',context,content_type="application/json")


@login_required
def singleIns(request):
    try:
        pet = Tamagochi.objects.get(user=request.user)
        pet_invitation_list=pet.play_innvitation.all()
        all_tama1 = Tamagochi.objects.all().order_by('-score1')
        all_tama2 = Tamagochi.objects.all().order_by('-score2')
        single_1 = []
        single_2 = []
        for tama1 in all_tama1:
            single_1.append(tama1)
            if len(single_1) == 3:
                break
        for tama2 in all_tama2:
            single_2.append(tama2)
            if len(single_2) == 3:
                break
        return render(request, 'game/singleIns.html', {'tama1': single_1,
                                                       'tama2': single_2,
                                                       'energy':pet.energy,
                                                       'msg':'Sorry! No Data! Be the first one to play this game!',
                                                       'pet_invitation_list':pet_invitation_list})
    except:
        raise Http404
