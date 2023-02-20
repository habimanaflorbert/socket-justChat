import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        print()
        print(self.scope.get('user').username)
        print()
        # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )
        # self.accept()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

   async  def disconnect(self, close_code):
     # Leave room group

            # async_to_sync(self.channel_layer.group_discard)(
            #     self.room_group_name, self.channel_name
            # )
            # Leave room group
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            
# Receive message from WebSocket
   async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        # # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type": "chat_message", "message": message}
        # )

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

        # Receive message from room group
   async def chat_message(self, event):
        # message = event["message"]

        # # Send message to WebSocket
        # self.send(text_data=json.dumps({"message": message}))

        message = event["message"]
        print()
        print(event)
        print()

        print()
        print(self.scope['user'])
        print()

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


from channels.consumer import AsyncConsumer

class EchoConsumer(AsyncConsumer):

   async  def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

   async  def websocket_receive(self, event):
       await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })