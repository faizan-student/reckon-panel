# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.roomGroupName = "group_chat_gfg"
#         await self.channel_layer.group_add(self.roomGroupName, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.roomGroupName, self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["username"]
#         await self.channel_layer.group_send(
#             self.roomGroupName,
#             {
#                 "type": "sendMessage",
#                 "message": message,
#                 "username": username,
#             },
#         )

#     async def sendMessage(self, event):
#         message = event["message"]
#         username = event["username"]
#         await self.send(
#             text_data=json.dumps({"message": message, "username": username})
#         )


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth import get_user_model
# from channels.db import database_sync_to_async
# from .models import ChatRoom, Message
# import re
# from datetime import datetime


# User = get_user_model()


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         # Sanitize: Replace all non-allowed chars with underscore
#         safe_room_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", self.room_name)
#         self.room_group_name = f"chat_{safe_room_name}"

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data["message"]
#         sender_username = data["sender"]
#         receiver_username = data["receiver"]

#         # Save message to database
#         await self.save_message(sender_username, receiver_username, message)

#         # Broadcast to group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {"type": "chat_message", "message": message, "sender": sender_username},
#         )

#     async def chat_message(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {"message": event["message"], "sender": event["sender"]}
#             )
#         )

#     @database_sync_to_async
#     def save_message(self, sender_username, receiver_username, message):
#         sender = User.objects.get(username=sender_username)
#         receiver = User.objects.get(username=receiver_username)

#         # Ensure a unique chat room exists
#         room_name = "_".join(sorted([sender_username, receiver_username]))
#         chatroom, created = ChatRoom.objects.get_or_create(name=room_name)
#         chatroom.participants.add(sender, receiver)

#         Message.objects.create(chat=chatroom, sender=sender, content=message)


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
import re
from datetime import datetime
from pytz import timezone

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        safe_room_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", self.room_name)
        self.room_group_name = f"chat_{safe_room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_username = data["sender"]
        receiver_username = data["receiver"]

        # Save message and get the saved timestamp
        timestamp = await self.save_message(sender_username, receiver_username, message)

        # Broadcast message with timestamp
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_username,
                "timestamp": timestamp,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender": event["sender"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)

        room_name = "_".join(sorted([sender_username, receiver_username]))
        chatroom, created = ChatRoom.objects.get_or_create(name=room_name)
        chatroom.participants.add(sender, receiver)

        msg = Message.objects.create(chat=chatroom, sender=sender, content=message)

        # Convert timestamp to Indian timezone
        india_tz = timezone("Asia/Kolkata")
        local_timestamp = msg.timestamp.astimezone(india_tz)

        # Return formatted Indian time (e.g., "May 14, 11:15 PM")
        return local_timestamp.strftime("%b %d, %I:%M %p")
