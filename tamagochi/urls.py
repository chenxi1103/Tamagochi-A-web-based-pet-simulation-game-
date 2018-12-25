"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('tamagochi/', include('tamagochi.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
import django.contrib.auth.views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.static import serve
from web.settings import MEDIA_ROOT
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    )

from tamagochi.views import *

urlpatterns = [
    path('',landing, name='landing'),
    path('signup',signup, name='signup'),
    path('login',login_view, name='login'),
    path('logout',logout_view, name = 'logout'),
    path('map',map, name='map'),
    path('hospital',hospital, name='hospital'),
    path('store',store, name='store'),
    path('playCastle',playCastle, name='playCastle'),
    path('egg',get_egg, name='egg'),
    #pop out message
    path('multiGame/get_message',get_message, name='get_message'),
    path('multiGame/dismiss_invitation',dismiss_invitation, name='dismiss_invitation'),
    path('multiGame/join_room',join_room, name='join_room'),
    # Home
    path('wallet',wallet, name='wallet'),
    path('warehouse',warehouse, name='warehouse'),
    path('friend',friend, name='friend'),
    path('search_friend/<name>', search_friend,name='search_friend'),
    path('invite_friend',invite_friend, name='invite_friend'),
    path('approve_friend',approve_friend, name='approve_friend'),
    path('dismiss_friend',dismiss_friend, name='dismiss_friend'),
    path('get_friend',get_friend, name='get_friend'),
    path('get_friendwaitlist',get_friendwaitlist, name='get_friendwaitlist'),
    url(r'^media/(?P<path>.*)', serve, {"document_root":MEDIA_ROOT}),
    path('confirmEmail/<str:username>/<slug:token>/',confirmEmail, name='confirm'),
    url(r'^resetPassword/$',PasswordResetView.as_view(template_name='authen/password_reset.html'),name='reset_password'),
    url(r'^resetPassword/done/$',PasswordResetDoneView.as_view(template_name='authen/password_reset_done.html'), name='password_reset_done'),
    url(r'^resetPassword/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(template_name='authen/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^resetPassword/complete/$',
        PasswordResetCompleteView.as_view(template_name='authen/password_reset_complete.html'), name='password_reset_complete'),
    path('add_item', add_item, name='add_item'),
    path('order_item', order_item, name='order_item'),
    path('feed',feed, name='feed'),
    path('feedFriend',feed_friend,name='feedFriend'),
    path('singleGame/instruction', singleIns, name='singleIns'),
    path('multiGame/instruction',multiIns, name='multiIns'),
    path('multiGame/check_status',check_status, name='check_status'),
    path('multiGame/guest_gameRoom/get_online_friends',get_online_friends, name='get_online_friends'),
    path('multiGame/guest_gameRoom/invite_friend_play',invite_friend_play, name='invite_friend_play'),
    path('gameroom/', gameRoom, name='gameRoom'),
    path('multiGame/guest_gameRoom/', guest_gameRoom, name='guest_gameRoom'),
    path('multiGame/racing',racingGame,name='racing'),
    path('singlegame/hitMouse',hitMouse,name='hitMouse'),
    url(r'^get_changes/?$', get_changes),
    path('singlegame/flappy',flappy,name='flappy'),
    path('singlegame/score1',score1,name='score1'),
    path('singlegame/score2',score2,name='score2'),
    path('othermap/<int:id>/',othermap, name='othermap'),
    path('get_player/', get_player, name='get_player'),
    path('lovewall/', lovewall, name='lovewall'),
    path('lovewall/search_friend/<name>', search_friend_marry,name='search_friend_marry'),
    path('lovewall/invite_friend',invite_friend_marry, name='invite_friend_marry'),
    path('lovewall/approve_friend',approve_friend_marry, name='approve_friend_marry'),
    path('lovewall/dismiss_friend',dismiss_friend_marry, name='dismiss_friend_marry'),
    path('lovewall/get_friendwaitlist',get_friendwaitlist_marry, name='get_friendwaitlist_marry'),
    path('lovewall/get_post',get_post, name='get_post'),
    path('lovewall/add_post',add_post, name='add_post'),
    path('lovewall/agree_post',agree_post, name='agree_post'),
    path('previous/', previous, name='previous'),
    path('near_by', near_by, name='near_by'),
    path('change_password', changePwd, name='changePwd'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
