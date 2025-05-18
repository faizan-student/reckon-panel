# chat/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name="chatrooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    attachment = models.ImageField(upload_to="chat_attachments/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"From {self.sender} in {self.chat}"
