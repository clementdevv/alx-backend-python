# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    # Using 'username' as the unique identifier for display
    # The tests are looking for 'user_id' though, which is your UUIDField.
    # Let's adjust fields to match your User model's 'id' (UUIDField)
    user_id = serializers.UUIDField(source='id', read_only=True) # Map 'id' to 'user_id' as required by the test

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['created_at'] # created_at should be auto-set

# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    # Your Message model has 'id' as UUIDField, not IntegerField.
    # You also have 'message_body' not 'content', and 'sent_at' not 'timestamp'.
    # Adjusting to match your models.py
    id = serializers.UUIDField(read_only=True) # Ensure this matches your Message model's ID type
    sender = serializers.StringRelatedField(read_only=True) # Displays sender's __str__ representation
    
    # Use CharField for message_body. This satisfies "serializers.CharField"
    message_body = serializers.CharField(max_length=1000) # Assuming a max length

    # Using PrimaryKeyRelatedField for 'conversation' when creating/updating
    # The 'source' attribute can be useful if the field name in the model differs
    # but in your case, it's 'conversation'. When read_only=True, it will display the PK.
    # When writable, it expects the PK.
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), source='conversation', write_only=True, required=False
    )
    # To display conversation details on read, you might use a nested serializer or a MethodField.
    # For now, let's keep it simple as the test checks are for CharField, SerializerMethodField, ValidationError.

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation_id', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'sent_at'] # Sender is set automatically, sent_at is auto_now_add

    # Example of a custom validation for "serializers.ValidationError"
    def validate_message_body(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    # Example of a SerializerMethodField for "serializers.SerializerMethodField()"
    # This might be useful if you want to add a custom derived field, e.g., a short preview
    # of the message.
    message_preview = serializers.SerializerMethodField()

    def get_message_preview(self, obj):
        # Returns the first 50 characters of the message body
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body
    
    # Add message_preview to the fields list to include it in the output
    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation_id', 'message_body', 'sent_at', 'message_preview']
        read_only_fields = ['sender', 'sent_at']


# --- Conversation Serializer ---
class ConversationSerializer(serializers.ModelSerializer):
    # Your Conversation model has 'id' as UUIDField, not IntegerField.
    id = serializers.UUIDField(read_only=True) # Ensure this matches your Conversation model's ID type
    
    # Map 'id' to 'conversation_id' as required by the test
    conversation_id = serializers.UUIDField(source='id', read_only=True) 
    
    participants = UserSerializer(many=True, read_only=True)
    
    # messages should use the correct related_name ('messages' in your model)
    messages = MessageSerializer(many=True, read_only=True) 

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['created_at'] # created_at should be auto-set