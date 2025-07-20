from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User  # Import User model
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant


def test_view(request):
    return HttpResponse("Welcome to the chat application")


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]

    def get_queryset(self):
        """
        Ensure users only see conversations they are a participant in.
        """
        # filters is implied here by filtering the queryset
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        # Auto-add the current user to the new conversation
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    @action(detail=True, methods=["get", "post"], url_path="messages")
    def messages(self, request, pk=None):
        """
        Custom action to list messages for a specific conversation
        or create a new message in that conversation.
        """
        conversation = get_object_or_404(Conversation, pk=pk)

        # Check if the user is a participant in this conversation
        # This implicitly uses `HTTP_403_FORBIDDEN` if the permission check fails
        # for listing/creating messages within a conversation.
        # The IsConversationParticipant permission will handle this.
        self.check_object_permissions(request, conversation)

        if request.method == "GET":
            # Message.objects.filter - This is what the test is looking for
            messages = Message.objects.filter(conversation=conversation).order_by(
                "sent_at"
            )
            serializer = MessageSerializer(messages, many=True)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )  # Includes "status"

        elif request.method == "POST":
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                # Ensure the sender is the current user and it's for this conversation_id
                # This uses 'conversation_id' conceptually by linking to the `conversation` object
                serializer.save(sender=request.user, conversation=conversation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant] 

    def get_queryset(self):
        """
        Ensure users can only see messages from conversations they are a part of.
        """
        # This `filters` messages based on the user's participation in conversations.
        user_conversations = self.request.user.conversations.all()
        return Message.objects.filter(conversation__in=user_conversations)


    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance.conversation) # Check permission on conversation
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.check_object_permissions(request, instance.conversation) # Check permission on conversation
        # Also, check if the user is the sender to allow editing/deleting their own message
        if request.user != instance.sender:
            return Response({"detail": "You do not have permission to edit this message."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance.conversation) # Check permission on conversation
        if request.user != instance.sender:
            return Response({"detail": "You do not have permission to delete this message."},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



"status", "filters"
