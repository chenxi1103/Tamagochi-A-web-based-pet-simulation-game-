from django.shortcuts import render
from tamagochi.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def store(request):
    foods = Item.objects.filter(category='food')
    toys = Item.objects.filter(category='toy')
    try:
        pet = Tamagochi.objects.get(user=request.user)
        pet_invitation_list=pet.play_innvitation.all()
        return render(request, 'event/store.html', {'foods': foods, 'toys': toys, 'pet': pet,'pet_invitation_list':pet_invitation_list})
    except:
        return render(request, 'authen/egg.html', {
            'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})


@login_required
def add_item(request):
    if 'POST' == request.method and 'item' in request.POST:
        try:
            item = Item.objects.get(name=request.POST['item'])
        except:
            return JsonResponse({'error': 'error'})

        response = {'success': render(request, 'event/single-item.html', {'item': item}).content.decode("utf-8"), 'price': item.price}
        return  JsonResponse(response)
    return JsonResponse({'error': 'error'})


@login_required
def order_item(request):
    if 'POST' == request.method:
        items = request.POST.getlist('items[]')
        try:
            tamagochi = Tamagochi.objects.get(user=request.user)
        except:
            return render(request, 'authen/egg.html', {
                'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})
        for name in items:
            item = Item.objects.get(name=name)
            Warehouse.objects.create(item=item, tamagochi=tamagochi)
            tamagochi.wallet -= item.price
        tamagochi.save()

        return JsonResponse({'success':'success'})
    else:
        return JsonResponse({'error':'error'})


@login_required
def hospital(request):
    medicine = Item.objects.filter(category='medicine')
    try:
        pet = Tamagochi.objects.get(user=request.user)
    except:
        return render(request, 'authen/egg.html', {
            'msg': 'Sorry! Your previous pet is dead! Please name your new Pet'})
    pet_invitation_list=pet.play_innvitation.all()
    return render(request, 'event/hospital.html', {'medicine': medicine, 'pet': pet,'pet_invitation_list': pet_invitation_list})
