# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.utils import timezone
from .forms import *
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *

# Create your tests here.
class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_egg(self):
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        self.client.login(username='testuser', password='password')
        url = reverse('egg')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_map(self):
        url = reverse('map')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_store(self):
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        self.client.login(username='testuser', password='password')
        url = reverse('store')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_playCastle(self):
        url = reverse('playCastle')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_get_friend(self):
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        tama = Tamagochi(user=user,name='testname')
        tama.save()

        self.client.login(username='testuser', password='password')
        url = reverse('get_friend')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class TestForms(TestCase):

    def test_signup_form(self):
        username = "testuser"
        email = 'abcd@gmail.com'
        password = '1234'
        confirm = '2345'
        form = SignupForm({'username': username,'email':email, 'password':password, 'confirm':confirm })
        self.assertFalse(form.is_valid())



class TestModels(TestCase):
    def setUp(self):
        self.client = Client()


    def test_create_tamagochi(self):

        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        self.client.login(username='testuser', password='password')

        tama = Tamagochi(name='name',user=user, gender='male',online=True)
        tama.save()

        self.assertTrue(len(Tamagochi.objects.filter(user=user,
                                                    name__iexact='name')) == 1)

    def test_create_item(self):


        item = Item(name='candy',price = '20', health='0',energy='20',happiness='0', category='food')
        item.save()

        self.assertTrue(len(Item.objects.filter(name__iexact='candy')) == 1)

    def test_buy_warehouse(self):

        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        self.client.login(username='testuser', password='password')

        tama = Tamagochi(name='name',user=user, gender='male',online=True)
        tama.save()

        item = Item(name='candy',price = '20', health='0',energy='20',happiness='0', category='food')
        item.save()

        ware = Warehouse(item=item,tamagochi=tama)
        ware.save()

        print(len(Warehouse.objects.filter(tamagochi=tama,item=item)))
        self.assertTrue(len(Warehouse.objects.filter(tamagochi=tama,
                                                    item=item)) == 1)
        url = reverse('warehouse')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
