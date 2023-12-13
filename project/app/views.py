from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, ChatSerializer, MessageSerializer
from .models import Chat, Message

class IndexView(APIView):
    def get(self, request):
        chat_list = Chat.objects.all()
        context = {
            'chat_list': chat_list,
        }
        return render(request=request, template_name='app/index.html', context=context)
    
class RoomView(APIView):
    def get(self, request, room_id):
        chat = Chat.objects.get(pk=int(room_id))
        if chat:
            message_list = Message.objects.filter(chat=room_id).order_by('-date_time')
            context = {
                'room_id': room_id,
                'message_list': message_list,
            }
            return render(request=request, template_name='app/room.html', context=context)
        else:
            return Response(data={'error': 'error'}, status=status.HTTP_404_NOT_FOUND)
        
class UserApiView(APIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
    
class ChatApiView(APIView):
    def get(self, request):
        chats = Chat.objects.all()
        chat_serializer = ChatSerializer(chats, many=True)
        return Response(data=chat_serializer.data, status=status.HTTP_200_OK)

class MessageApiView(APIView):
    def get(self, request):
        messages = Message.objects.all()
        message_serializer = MessageSerializer(messages, many=True)
        return Response(data=message_serializer.data, status=status.HTTP_200_OK)

class NewChatView(APIView):
    def get(self, request):
        return render(request=request, template_name='app/newchat.html')
    
    def post(self, request):
        chat_name = request.data['chat_name']
        Chat.objects.create(chat_name=chat_name)
        return Response(data=request.data, status=status.HTTP_201_CREATED)