from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requests import get
from tamagochi.forms import *
from django.contrib.auth import authenticate
from django.http import Http404


@login_required
def map(request):
    user = request.user
    try:
        pet_self = Tamagochi.objects.get(user=user)
    except:
        return render(request, 'authen/egg.html',{'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})
    pet_invitation_list=pet_self.play_innvitation.all()

    latitude = pet_self.latitude
    longitude = pet_self.longitude
    weather_id = get_weather(latitude,longitude)

    weather_url = '/static/images/weather/'+ weather_id +'.png'
    return render(request, 'authen/map.html', {"pet_self":pet_self,'pet_invitation_list':pet_invitation_list, 'weather':weather_url})


@login_required
def lovewall(request):
    try:
        message=""
        pet_self = Tamagochi.objects.get(user=request.user)
        return render(request, 'marriage/lovewall.html',{'pet_self': pet_self,"message":message})
    except:
        return render(request, 'authen/egg.html',{'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})


@login_required
def changePwd(request):
    context = {}
    try:
        if request.method == 'GET':
            context['form'] = changePassword()
            return render(request, 'authen/change_password.html', context)
        form = changePassword(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'authen/change_password.html', context)
        oldPwd = form.cleaned_data['oldPwd']
        user = authenticate(username=request.user.username, password=oldPwd)
        if user:
            user.set_password(form.cleaned_data['newPwd1'])
            user.save()
            return render(request,'authen/password_reset_complete.html')
        else:
            context['errors'] = 'Sorry! You old password is wrong!'
            return render(request,'authen/change_password.html', context)
    except:
        raise Http404


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_weather(latitude,longitude):
    weather1 = get("https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID=2af708516c0a5a89ff92ec1cc0af99f3".format(latitude, longitude)).json()
    icon_id = weather1['weather'][0]['icon']
    return icon_id
