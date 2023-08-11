import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       self.room_group_name = 'Test-room'

       await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
       )

       await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("DisConnected")
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        action = text_data_json['action']
            
        if action in ['new-offer', 'new-answer']:
            receiver_channel_name = text_data_json['message']['receiver_channel_name']  # Correct the key name here
            text_data_json['message']['receiver_channel_name'] = self.channel_name  # Correct the key name here
            await self.channel_layer.send(
                receiver_channel_name ,
                {
                    'type': 'send.sdp',
                    'message' : text_data_json
                }
            )
            return
            
        text_data_json['message']['receiver_channel_name'] = self.channel_name  # Correct the key name here

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'message' : text_data_json
            }
        )




    async def send_sdp(self, event):
        # print(str(event['message'])+"<----")
        message = event['message']

        await self.send(text_data=json.dumps(message))