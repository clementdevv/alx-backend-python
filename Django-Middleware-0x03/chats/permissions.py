# messaging_app/chats/permissions.py

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message # Import models if needed

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access or modify it and its related messages.
    """

    def has_permission(self, request, view):
        # Allow authenticated users to perform actions on the list view
        # or to create new conversations.
        # This addresses "user.is_authenticated" for overall access.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj will be a Conversation instance or a Message instance
        # if used on MessageViewSet, obj will be a Message.
        # If obj is a Message, get its conversation.
        conversation = obj if isinstance(obj, Conversation) else obj.conversation

        # Check if the user is a participant in the conversation
        if request.user in conversation.participants.all():
            # For GET, HEAD, OPTIONS (safe methods), if participant, allow
            if request.method in permissions.SAFE_METHODS:
                return True
            # For PUT, PATCH, DELETE, if participant, allow modification
            # This directly addresses "PUT", "PATCH", "DELETE"
            elif request.method in ['PUT', 'PATCH', 'DELETE']:
                # For messages, additionally check if the user is the sender for modification/deletion
                if isinstance(obj, Message) and request.method in ['PUT', 'PATCH', 'DELETE']:
                    return request.user == obj.sender
                return True
        
        # If not a participant, deny access.
        # This would implicitly lead to a 403 Forbidden.
        # You could explicitly raise PermissionDenied if you prefer custom error messages.
        # raise PermissionDenied("You are not a participant in this conversation.")
        return False

# You might still keep this if you have specific message-level permissions
# but IsConversationParticipant should cover most cases if applied correctly.
class IsMessageSenderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow senders of a message to edit/delete it,
    but allows anyone in the conversation to read it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (if part of conversation)
        if request.method in permissions.SAFE_METHODS:
            # Check if the user is a participant of the message's conversation
            return request.user in obj.conversation.participants.all()

        # Write permissions are only allowed to the sender of the message.
        return obj.sender == request.user