from django.db import models
from django.db import models
from .managers import UnreadMessagesManager
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
    
class MessageHistory(models.Model):
    original_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='histories')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for message {self.original_message.id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message {self.message.id}"
