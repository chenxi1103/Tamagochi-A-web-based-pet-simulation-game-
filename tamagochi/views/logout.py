from django.shortcuts import redirect
from tamagochi.forms import *
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def logout_view(request):
    log = LoginLogoutLog.objects.get(user=request.user)
    print(request.user,'user')
    log.logout_time = timezone.now()
    print(log.logout_time, log.login_time, 'in and out ')
    if log.length is not None:
        log.length = log.length + (log.logout_time - log.login_time)
    else:
        log.length = (log.logout_time - log.login_time)

    print(type(log.length),'length')
    print(type(log.logout_time),'logout')
    log.temp = None
    log.save()
    pet=Tamagochi.objects.get(user=request.user)
    pet.online=False
    pet.save()
    auth_logout(request)
    return redirect('landing')
