from django.db.models import Count, Q

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Message

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)

    users_with_unread = []

    for user in users:
        unread_count = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()

        users_with_unread.append({
            "user": user,
            "unread_count": unread_count
        })

    return render(request, "user_list.html", {
        "users_with_unread": users_with_unread
    })

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    )

    # Mark unread as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    room_name = f"{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}"

    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages,
        'room_name': room_name
    })
