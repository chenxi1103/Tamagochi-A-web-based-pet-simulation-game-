from django.shortcuts import render
from tamagochi.forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import geocoder
from requests import get


@login_required
def wallet(request):
    try:
        pet_self=Tamagochi.objects.get(user=request.user)
        pet_invitation_list=pet_self.play_innvitation.all()
        context={"pet_self":pet_self,'pet_invitation_list':pet_invitation_list}
        return render(request, 'event/home-wallet.html', context)
    except:
        return render(request, 'authen/egg.html', {
            'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})


@login_required
def get_changes(request):
    try:
        pet_self = Tamagochi.objects.get(user=request.user)
        log = LoginLogoutLog.objects.get(user=request.user)
        if log.temp is None:
            diff = timezone.now() - log.login_time
        else:
            # first time login and hasn't logged OUT
            diff = timezone.now() - log.temp
        # change values
        diff_min = int(diff.total_seconds() / 1)
        pet_self.energy = int(pet_self.energy - diff_min * 0.00000005)
        if pet_self.energy < 0:
            pet_self.energy = 0

        elif pet_self.energy > 100:
            pet_self.energy = 100

        pet_self.happiness = int(pet_self.happiness - diff_min  * 0.00000003)

        if pet_self.happiness < 0:
            pet_self.happiness = 0
        elif pet_self.happiness > 100:
            pet_self.happiness = 100

        # health relevant to weather:
        latitude = pet_self.latitude
        longitude = pet_self.longitude
        weather_id = get_weather(latitude,longitude)

        if  "04" in weather_id or  "09" in weather_id or "10" in weather_id:
            pet_self.health = int(pet_self.health - diff_min * 0.0004)
        elif '11' in weather_id or '13' in weather_id:
            pet_self.health = int(pet_self.health - diff_min * 0.0009)
        elif '50' in weather_id:
            pet_self.health = int(pet_self.health - diff_min * 1)

        if pet_self.health < 0:
            pet_self.health = 0
        elif pet_self.health > 100:
            pet_self.health = 100

        if log.length is not None:
            if log.temp is not None:
                log.length = log.length + timezone.now() - log.temp
        else:
            log.length = timezone.now() - log.login_time

        log.temp = timezone.now()
        age = log.length
        log.save()

        # show
        energy_percent = "{0:.0f}%".format(pet_self.energy)
        happiness_percent = "{0:.0f}%".format(pet_self.happiness)
        health_percent = "{0:.0f}%".format(pet_self.health)

        day, hour, minutes = age.days, age.seconds // 3600, (
                    age.seconds // 60) % 60
        age = '{:02d} D {:02d} H {:02d} M'.format(day, hour, minutes)
        pet_self.age = age

        if(hour >= 1 and hour < 2 and day == 0):
            pet_self.level = 2
            pet_self.apperance = '/tamaEvolve/' + str(pet_self.apperanceNum) + '/2.png'
        elif(hour >= 2 and hour < 4 and day == 0):
            pet_self.level = 3
            pet_self.apperance = '/tamaEvolve/' + str(pet_self.apperanceNum) + '/3.png'
        elif(hour >= 4 or day >= 1):

            pet_self.level = 4
            pet_self.apperance = '/tamaEvolve/' + str(pet_self.apperanceNum) + '/4.png'
        else:
            pet_self.level = 1
            pet_self.apperance = '/tamaEvolve/' + str(pet_self.apperanceNum) + '/1.png'

        pet_self.save()
        if pet_self.energy == 0 or pet_self.happiness == 0 or pet_self.health == 0:
            pet_dead = previousTama(user=request.user,
                                    name=pet_self.name,
                                    dead_date=timezone.now(),
                                    gender=pet_self.gender,
                                    apperance=pet_self.apperance,
                                    level=pet_self.level,
                                    age=pet_self.age)
            pet_dead.save()
            pet_self.delete()
        context = {"pet_self": pet_self}
        return render(request, 'status.json', context,
                      content_type='application/json')
    except:
        return render(request, 'authen/egg.html', {
            'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})


@login_required
def previous(request):
    pet_self = Tamagochi.objects.get(user=request.user)
    previous = previousTama.objects.filter(user=request.user)
    if len(previous) == 0:
        return render(request,'event/previous.html', {'pet_self': pet_self,
                                                      'msg': 'Great! You do not have any dead pet!'})
    return render(request, 'event/previous.html',
                  {'pet_self': pet_self,
                   'pet_dead': previous})


def get_latlong():
    g = geocoder.ip('me')
    ip = g.ip
    latlong = get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')
    return(latlong)


def get_weather(latitude,longitude):
    weather1 = get("https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID=2af708516c0a5a89ff92ec1cc0af99f3".format(latitude, longitude)).json()
    icon_id = weather1['weather'][0]['icon']
    return icon_id
