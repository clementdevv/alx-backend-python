# messaging_app/chats/filters.py

import django_filters
from .models import Message, Conversation, User # Ensure User is imported if you need to filter by user details

class MessageFilter(django_filters.FilterSet):
    """
    Filter for Messages:
    - by conversation ID
    - by sender (user) username or ID
    - within a time range (sent_at_after, sent_at_before)
    """
    # Filter by conversation ID
    conversation = django_filters.UUIDFilter(field_name='conversation__id', lookup_expr='exact')

    # Filter messages sent by a specific user (by username)
    sender_username = django_filters.CharFilter(
        field_name='sender__username', lookup_expr='icontains',
        label="Filter by sender's username (case-insensitive contains)"
    )
    
    # Filter messages sent by a specific user (by ID)
    sender_id = django_filters.UUIDFilter(
        field_name='sender__id', lookup_expr='exact',
        label="Filter by sender's ID"
    )

    # Filter messages sent after a specific datetime
    sent_at_after = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='gte',
        label='Messages sent at or after (YYYY-MM-DDTHH:MM:SSZ)'
    )

    # Filter messages sent before a specific datetime
    sent_at_before = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='lte',
        label='Messages sent at or before (YYYY-MM-DDTHH:MM:SSZ)'
    )

    class Meta:
        model = Message
        # You can specify fields directly or use '__all__'
        # fields = ['conversation', 'sender', 'sent_at'] # Can be more specific
        fields = {
            'conversation': ['exact'],
            'sender': ['exact'], # Filter by sender's UUID
            'sent_at': ['gte', 'lte'],
        }
        # The custom filters (sender_username, sent_at_after, sent_at_before) are added explicitly.