import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer handling real-time private chat functionality.

    Features:
    - Message sending
    - Typing indicators
    - Read receipts
    - Real-time unread badge updates
    """

    async def connect(self):
        """
        Handles WebSocket connection.
        Adds user to private chat group and personal notification group.
        Rejects anonymous users.
        """
        self.user = self.scope["user"]

        # Reject anonymous users
        if self.user.is_anonymous:
            await self.close()
            return

        # Private chat room (between two users)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join private room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Join personal notification group (for unread updates)
        self.user_group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave private room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Leave personal group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles incoming WebSocket messages.
        Supports:
        - typing
        - stop_typing
        - message
        - read
        """
        data = json.loads(text_data)
        event_type = data.get("type")

        # TYPING EVENT
        if event_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_event",
                    "user": self.user.username
                }
            )

        # STOP TYPING
        elif event_type == "stop_typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "stop_typing_event",
                    "user": self.user.username
                }
            )

        # SEND MESSAGE
        elif event_type == "message":
            message = data.get("message", "").strip()
            receiver_id = data.get("receiver_id")

            if not message or not receiver_id:
                return

            receiver = await database_sync_to_async(User.objects.get)(id=receiver_id)

            # Save message
            msg = await database_sync_to_async(Message.objects.create)(
                sender=self.user,
                receiver=receiver,
                content=message
            )

            # Send message to private chat room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": self.user.username,
                    "sender_id": self.user.id,
                    "message_id": msg.id
                }
            )

            #  Notify receiver about unread message
            await self.channel_layer.group_send(
                f"user_{receiver.id}",
                {
                    "type": "unread_update_event",
                    "sender_id": self.user.id
                }
            )

        # READ RECEIPT
        elif event_type == "read":
            message_ids = data.get("message_ids", [])

            if not message_ids:
                return

            # Update messages as read
            await database_sync_to_async(
                Message.objects.filter(
                    id__in=message_ids,
                    receiver=self.user
                ).update
            )(is_read=True)

            # Notify sender in chat room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "read_receipt_event",
                    "message_ids": message_ids,
                    "reader_id": self.user.id
                }
            )

    # HANDLE TYPING
    async def typing_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user": event["user"]
        }))

    # HANDLE STOP TYPING
    async def stop_typing_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "stop_typing",
            "user": event["user"]
        }))

    # HANDLE MESSAGE
    async def chat_message(self, event):
        """
        Sends chat message to WebSocket client.
        """
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"],
            "sender": event["sender"],
            "sender_id": event["sender_id"],
            "message_id": event["message_id"]
        }))

    # HANDLE READ RECEIPT
    async def read_receipt_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "read_receipt",
            "message_ids": event["message_ids"],
            "reader_id": event["reader_id"]
        }))

    # HANDLE UNREAD BADGE UPDATE
    async def unread_update_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "unread_update",
            "sender_id": event["sender_id"]
        }))
