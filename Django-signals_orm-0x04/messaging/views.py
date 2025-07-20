from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Message
from django.shortcuts import render
from django.views.decorators.cache import cache_page




@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect("home") 

def conversation_thread(request):
    messages = Message.objects.filter(sender=request.user).select_related('receiver').prefetch_related('histories')
    return render(request, 'messaging/thread.html', {'messages': messages})


def get_threaded_messages(parent):
    replies = Message.objects.filter(parent_message=parent).select_related('sender', 'receiver')
    thread = []
    for reply in replies:
        thread.append(reply)
        thread += get_threaded_messages(reply)
    return thread

def view_message_thread(request, message_id):
    parent = Message.objects.select_related('sender', 'receiver').get(id=message_id)
    thread = get_threaded_messages(parent)
    return render(request, 'messaging/thread_detail.html', {'parent': parent, 'thread': thread})

def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})

@cache_page(60)  # 60 seconds
def conversation_view(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender').only('id', 'content', 'timestamp')
    return render(request, 'messaging/conversations.html', {'messages': messages})
