from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='chatrooms')
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return self.name