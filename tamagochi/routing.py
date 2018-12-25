from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/racing/(?P<room_name>[^/]+)/(?P<user_id>[^/]+)/$', consumers.RaceConsumer),
    url(r'^ws/room/(?P<room_name>[^/]+)/(?P<user_id>[^/]+)/$', consumers.RoomConsumer),
]