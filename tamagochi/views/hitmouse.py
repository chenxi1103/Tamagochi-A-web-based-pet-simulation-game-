from django.shortcuts import render
from tamagochi.models import *
from django.http import Http404
from django.contrib.auth.decorators import login_required


@login_required
def hitMouse(request):
    try:
        pet = Tamagochi.objects.get(user=request.user)
        return render(request, 'game/singlegame2.html', {'pet':pet})
    except:
        raise Http404


@login_required
def score2(request):
    if 'score' not in request.POST or not request.POST['score']:
        raise Http404
    else:
        score2 = request.POST['score']
        pet_self = Tamagochi.objects.get(user=request.user)
        pet_self.score2 = max(int(score2), pet_self.score2)
        pet_self.wallet += int(score2)
        pet_self.energy -= 2
        if pet_self.happiness < 95:
            pet_self.happiness += 5
        else:
            pet_self.happiness = 100
        pet_self.save()
        return render(request, 'game/singleIns.html', {})










