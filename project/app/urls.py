from django.urls import path

from .views import IndexView, RoomView, UserApiView, ChatApiView, MessageApiView

urlpatterns = [
    path('user-api/', UserApiView.as_view(), name='user-api'),
    path('chat-api/', ChatApiView.as_view(), name='chat-api'),
    path('message-api/', MessageApiView.as_view(), name='message-api'),
    path('index/', IndexView.as_view(), name='index'),
    path('<str:room_id>/', RoomView.as_view(), name='room'),
]