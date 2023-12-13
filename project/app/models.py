from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    chat_name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.chat_name
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text