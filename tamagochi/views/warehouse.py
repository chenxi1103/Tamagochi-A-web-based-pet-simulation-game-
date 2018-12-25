from django.shortcuts import render
from tamagochi.models import *
from django.contrib.auth.decorators import login_required


@login_required
def warehouse(request):
    try:
        pet_self=Tamagochi.objects.get(user=request.user)
        pet_invitation_list=pet_self.play_innvitation.all()
        ware = Warehouse.objects.filter(tamagochi=pet_self) | Warehouse.objects.filter(tamagochi=pet_self.partner)
        context={"pet_self":pet_self, "items":ware,'pet_invitation_list':pet_invitation_list}
        return render(request, 'event/home-warehouse.html', context)
    except Exception as e:
        print(e)
        return render(request, 'authen/egg.html', {
            'msg': 'Sorry! Your previous pet is dead! Please name your new Pet!'})
