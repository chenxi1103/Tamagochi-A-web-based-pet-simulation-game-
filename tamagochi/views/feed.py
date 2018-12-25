from django.shortcuts import render
from tamagochi.models import *
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required


@login_required
def feed(request):
    if 'POST' == request.method:
        id = request.POST['item_id']
        try:
            pet_self = Tamagochi.objects.get(user=request.user)
            try:
                ware = Warehouse.objects.get(id=id)
                use = ware.item
                if use.energy is not None:
                    (pet_self.energy) = int(pet_self.energy) + int(use.energy)
                if use.health is not None:
                    (pet_self.health) = int(pet_self.health) + int(use.health)
                if use.happiness is not None:
                    (pet_self.happiness) = int(pet_self.happiness) + int(use.happiness)
                ware.delete()
                pet_self.save()
                return JsonResponse({'message': ''})
            except Exception as e:
                return JsonResponse({'message': 'Oops! This item has already been used. '})
        except:
            return render(request, 'authen/egg.html', {
                'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})
    else:
        raise Http404


@login_required
def feed_friend(request):
    if 'POST' == request.method:
        id = request.POST['item_id']
        friend_id = request.POST['friend_id']
        try:
            pet_self = Tamagochi.objects.get(user=request.user)
            friend = Tamagochi.objects.get(id=friend_id)
            try:
                ware = Warehouse.objects.get(id=id)
                use = ware.item
                if use.energy is not None:
                    (friend.energy) = int(friend.energy) + int(use.energy)
                    if friend.energy >= 100:
                        friend.energy = 100
                if use.health is not None:
                    (friend.health) = int(friend.health) + int(use.health)
                    if friend.health >= 100:
                        friend.health = 100
                if use.happiness is not None:
                    (friend.happiness) = int(friend.happiness) + int(use.happiness)
                    if friend.happiness >= 100:
                        friend.happiness = 100
                ware.delete()
                pet_self.save()
                friend.save()
                return JsonResponse({'message': ''})
            except Exception as e:
                return JsonResponse({'message': 'Oops! This item has already been used. '})
        except:
            return render(request, 'authen/egg.html', {
                'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})
    else:
        raise Http404
