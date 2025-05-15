# from django.shortcuts import render, redirect


# def chatPage(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return redirect("login")
#     context = {}
#     return render(request, "chat/chat.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()


# def chatPage(request, username):
#     if not request.user.is_authenticated:
#         return redirect("login")

#     receiver = get_object_or_404(User, username=username)
#     room_name = "_".join(sorted([str(request.user.username), str(receiver.username)]))
#     chatroom, created = ChatRoom.objects.get_or_create(name=room_name)
#     chatroom.participants.add(request.user, receiver)

#     messages = Message.objects.filter(chat=chatroom).order_by("timestamp")

#     return render(
#         request,
#         "chat/chat.html",
#         {
#             "receiver": receiver,
#             "room_name": room_name,
#             "messages": messages,
#         },
#     )


def chatPage(request, username):
    if not request.user.is_authenticated:
        return redirect("login")

    receiver = get_object_or_404(User, username=username)
    room_name = "_".join(sorted([str(request.user.username), str(receiver.username)]))
    chatroom, created = ChatRoom.objects.get_or_create(name=room_name)
    chatroom.participants.add(request.user, receiver)

    messages = Message.objects.filter(chat=chatroom).order_by("timestamp")
    all_users = User.objects.exclude(id=request.user.id)

    return render(
        request,
        "chat/chat.html",
        {
            "receiver": receiver,
            "room_name": room_name,
            "messages": messages,
            "all_users": all_users,
        },
    )
