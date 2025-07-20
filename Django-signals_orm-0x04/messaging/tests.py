from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTest(TestCase):
    def test_notification_created_on_message_send(self):
        sender = User.objects.create_user(username='alice', password='pass')
        receiver = User.objects.create_user(username='bob', password='pass')
        message = Message.objects.create(sender=sender, receiver=receiver, content="Hello Bob!")

        notification_exists = Notification.objects.filter(user=receiver, message=message).exists()
        self.assertTrue(notification_exists)

