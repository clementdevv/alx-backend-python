from rest_framework import serializers
from .models import User, Conversation, Message


# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sender = serializers.StringRelatedField()  
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'content', 'timestamp']


# --- Conversation Serializer ---
class ConversationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)     
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(source='message_set', many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
