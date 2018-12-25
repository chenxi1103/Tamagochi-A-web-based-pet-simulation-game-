from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *
from django.http import HttpResponse, Http404, JsonResponse
import datetime

class RaceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if text_data_json['message'] == 'score':

            text = text_data_json['text']
            user = User.objects.get(id=self.user_id)
            tamagochi = Tamagochi.objects.get(user=user)
            room = Gameroom.objects.get(id=self.room_name)
            score = int(text_data_json['score'])
            wallet = 1000 // score

            if not room.winner:
                room.winner = tamagochi
                room.save()
                text += '&nbsp&nbsp&nbsp<span class="winner">Winner!</span>'

            record = Gamerecord.objects.get(player=tamagochi, room=room)
            record.score = text
            record.save()

            tamagochi.energy -= 5
            tamagochi.wallet += wallet

            if tamagochi.score3 == 0 or tamagochi.score3 > score:
                tamagochi.score3 = score
            tamagochi.save()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'race_message',
                    'message': 'score', 
                    'user': self.user_id,
                    'text': text, 
                    'wallet': wallet
                }
            )
              
        elif text_data_json['message'] == 'move':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'race_message',
                    'message': 'move',
                    'user': self.user_id,
                    'text': text_data_json['text'],
                }
            )

    # Receive message from room group
    async def race_message(self, event):
        message = {key: value for key, value in event.items() if key != 'type'}

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': 'add',
                'text': self.user_id,
            }
        )

        await self.accept()

    async def disconnect(self, close_code):

        user = User.objects.get(id=self.user_id)
        tamagochi = Tamagochi.objects.get(user=user)
        tamagochi.game_status = 'Not Ready'
        tamagochi.save()

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['message'] == 'ready':
            user = User.objects.get(id=self.user_id)
            tamagochi = Tamagochi.objects.get(user=user)
            tamagochi.game_status = 'Ready!'
            tamagochi.save()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_message',
                    'message': 'ready',
                    'text': self.user_id,
                }
            )

        elif text_data_json['message'] == 'start':
            try:
                user = User.objects.get(id=self.user_id)
                tamagochi = Tamagochi.objects.get(user=user)
                room = Gameroom.objects.get(id=tamagochi.current_game_room_id)
            except Exception as e:
                raise Http404
            tamagochi.game_status = 'Ready!'
            room.game_time = datetime.datetime.now()
            room.room_active = False
            tamagochi.save()
            room.save()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_message',
                    'message': 'start',
                    'text': self.user_id,
                }
            )

        elif text_data_json['message'] == 'timeup':
            try:
                user = User.objects.get(id=self.user_id)
                tamagochi = Tamagochi.objects.get(user=user)
                room = Gameroom.objects.get(id=tamagochi.current_game_room_id)
            except Exception as e:
                raise Http404
            room.room_active = False
            room.save()

    # Receive message from room group
    async def room_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'], 
            'text': event['text']
        }))
