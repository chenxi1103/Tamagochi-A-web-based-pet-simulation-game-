from django.shortcuts import render
from django.http import HttpResponse, Http404
from tamagochi.models import *


def add_post(request):
    if 'post' not in request.POST or not request.POST['post']:
        raise Http404
    else:
        pet_self=Tamagochi.objects.get(user=request.user)
        new_post = Post(text=request.POST['post'],pet=pet_self)
        new_post.save()
    return HttpResponse("")


def get_post(request):
    posts = Post.objects.all().order_by('agree_time')
    context = {"posts":posts}
    return render(request, 'posts.json', context, content_type='application/json')


def agree_post(request):
    if not 'post_id' in request.POST or not request.POST['post_id']:
        raise Http404
    else:
        user=User.objects.get(username=request.user)
        new_post=Post.objects.get(id=request.POST['post_id'])
        if user not in new_post.agree_pet.all():
            new_post.agree_pet.add(user)
            new_post.agree_number=len(new_post.agree_pet.all())
            new_post.save()
    return HttpResponse("")
