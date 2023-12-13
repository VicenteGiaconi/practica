import json

from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from rest_framework_simplejwt.tokens import AccessToken

from .models import Chat, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat_id = text_data_json['room_id']
        token = AccessToken(text_data_json['user_token'])
        chat = Chat.objects.get(pk=chat_id)
        user = User.objects.get(pk=token.payload['user_id'])
        Message.objects.create(chat=chat, text=message, sender=user)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message",
                                   "message": message,
                                   'user_token': text_data_json['user_token'],
                                   }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        token = event['user_token']

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message,
                                        'user_token': token
                                        }))