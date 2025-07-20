from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.pk:  # Only check if it's an update
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                instance.edited = True
                MessageHistory.objects.create(
                    original_message=old_message,
                    old_content=old_message.content
                )
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    from .models import Message, Notification, MessageHistory
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(original_message__sender=instance).delete()