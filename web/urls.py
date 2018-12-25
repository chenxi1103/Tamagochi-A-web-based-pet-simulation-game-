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

import tamagochi.views

urlpatterns = [
    path('tamagochi/', include('tamagochi.urls')),
    path('admin/', admin.site.urls),
    path('', tamagochi.views.landing,name='landing'),
    path('map',tamagochi.views.map, name='map'),
    path('egg',tamagochi.views.get_egg, name='get_egg'),
    # path('password',tamagochi.views.change_password, name = 'change_password'),
]