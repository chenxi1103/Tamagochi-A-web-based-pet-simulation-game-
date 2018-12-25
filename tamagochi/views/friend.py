from django.shortcuts import render
from tamagochi.models import *
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required


@login_required
def friend(request):
    try:
        pet_self=Tamagochi.objects.get(user=request.user)
        friend_waitlist = pet_self.friend_waitlist.all()
        friend_waitlist_number=len(friend_waitlist)
        pet_invitation_list = pet_self.play_innvitation.all()
        context={"pet_self" : pet_self, "friend_waitlist":friend_waitlist,\
        'pet_invitation_list': pet_invitation_list,"friend_waitlist_number": friend_waitlist_number}
        return render(request, 'event/home-friend.html',context)
    except:
        return render(request, 'authen/egg.html', {
            'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})


@login_required
def search_friend(request,name):
    friends_searched = Tamagochi.objects.filter(name__startswith=name).exclude(user=request.user)
    context = {"friends":friends_searched,"name":name}
    return render(request, 'friends.json', context, content_type='application/json')


@login_required
def near_by(request):
    self_pet = Tamagochi.objects.get(user=request.user)
    friends_searched = Tamagochi.objects.filter(latitude__range=(int(self_pet.latitude)-1,
                                                                 int(self_pet.latitude)+1)).filter(longitude__range=(int(self_pet.longitude)-1, int(self_pet.longitude)+1)).exclude(user=request.user)
    context = {"friends":friends_searched}
    return render(request, 'friends.json', context, content_type='application/json')


@login_required
def search_friend_marry(request,name):
    pet_self=Tamagochi.objects.get(user=request.user)
    self_gender=pet_self.gender
    if self_gender == "Female":
        friend_other_gender=pet_self.friends.all().exclude(gender='Female')
    if self_gender == "Male":
        friend_other_gender=pet_self.friends.all().exclude(gender='Male')
    friends_searched = friend_other_gender.filter(name__startswith=name)
    context = {"friends":friends_searched,"name":name}
    return render(request, 'friends.json', context, content_type='application/json')


@login_required
def invite_friend(request):
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self=Tamagochi.objects.get(user=request.user)
        # invite friend=put yourself on your friend's waitlist
        pet_friend.friend_waitlist.add(pet_self)
        pet_friend.save()
        print('waitlist added')
        return HttpResponse("")


@login_required
def invite_friend_marry(request):
    message = ""
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self=Tamagochi.objects.get(user=request.user)
        if pet_self.partner != None:
            message="You have already got a partner."
            print("You have already got a partner")
        elif pet_friend.partner != None:
            message = 'Your friend has already got a partner! '
        else:
            if pet_self.level >= 2 and pet_friend.level >= 2:
                pet_friend.partner_waitlist.add(pet_self)
                pet_friend.save()
                print('waitlist added')
            else:
                message = "You are too young to marry. Both pets level need to be larger than 2."
        # invite friend=put yourself on your friend's waitlist
        context={"message":message}
        print(context)
        return render(request, 'friends-marry.json', context, content_type='application/json')


@login_required
def approve_friend(request):
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self = Tamagochi.objects.get(user=request.user)
        # approve friend=remove yourself from your friend's waitlist
        # and put yourself on your friend's list, put your friend on your list
        pet_friend.friends.add(pet_self)
        pet_self.friends.add(pet_friend)
        pet_self.friend_waitlist.remove(pet_friend)
        pet_friend.save()
        pet_self.save()
        print('approved')
        return HttpResponse("")


@login_required
def approve_friend_marry(request):
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        message = ''
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self = Tamagochi.objects.get(user=request.user)
        # approve friend=remove yourself from your friend's waitlist
        # and put yourself on your friend's list, put your friend on your list
        if pet_self.partner != None:
            message = 'You have already got a partner! '
        elif pet_friend.partner != None:
            message = 'Your friend has already got a partner! '
        else:
            pet_friend.partner = pet_self
            pet_self.partner = pet_friend
            pet_self.partner_waitlist.remove(pet_friend)
            pet_friend.save()
            pet_self.save()

        context={"message":message}
        print(context)
        return render(request, 'friends-marry.json', context, content_type='application/json')


@login_required
def dismiss_friend(request):
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self = Tamagochi.objects.get(user=request.user)
        # dismiss friend=remove yourself from your friend's waitlist
        pet_friend.friend_waitlist.remove(pet_self)
        pet_self.friend_waitlist.remove(pet_friend)
        pet_friend.save()
        pet_self.save()
        return HttpResponse("")


@login_required
def dismiss_friend_marry(request):
    if 'friend_id' not in request.POST or not request.POST['friend_id']:
        raise Http404
    else:
        pet_friend = Tamagochi.objects.get(id=request.POST['friend_id'])
        pet_self=Tamagochi.objects.get(user=request.user)
        # dismiss friend = remove yourself from your friend's waitlist
        pet_friend.partner_waitlist.remove(pet_self)
        pet_self.partner_waitlist.remove(pet_friend)
        pet_friend.save()
        pet_self.save()
        return HttpResponse("")


@login_required
def get_friend(request):
    user = Tamagochi.objects.get(user=request.user)
    friends = user.friends.all()
    context = {"friends":friends}
    return render(request, 'friends2.json', context, content_type='application/json')


@login_required
def get_friendwaitlist(request):
    user = Tamagochi.objects.get(user=request.user)
    friend_waitlist = user.friend_waitlist.all()
    context = {"friends":friend_waitlist,"waitlist_number":len(friend_waitlist)}
    return render(request, 'friends3.json', context, content_type='application/json')


@login_required
def get_friendwaitlist_marry(request):
    user = Tamagochi.objects.get(user=request.user)
    friend_waitlist = user.partner_waitlist.all()
    context = {"friends":friend_waitlist,"waitlist_number" : len(friend_waitlist)}
    return render(request, 'friends3.json', context, content_type='application/json')


@login_required
def othermap(request,id):
    try:
        otherpet = Tamagochi.objects.get(pk=id)
    except:
        raise Http404

    try:
        pet_self = Tamagochi.objects.get(user=request.user)
        pet_invitation_list=pet_self.play_innvitation.all()
        print(otherpet.health,'health')
        ware = Warehouse.objects.filter(tamagochi=pet_self) | Warehouse.objects.filter(tamagochi=pet_self.partner)
        health = "{0:.0f}%".format(otherpet.health)
        happiness = "{0:.0f}%".format(otherpet.happiness)
        energy = "{0:.0f}%".format(otherpet.energy)

        context={"health": health, "happiness": happiness, "energy" : energy,
        "pet_self": otherpet, "items":ware, 'pet_invitation_list':pet_invitation_list}
        return render(request, 'event/other-map.html', context)
    except:
        return render(request, 'authen/egg.html', {
            'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})
