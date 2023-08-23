import json
from datetime import datetime, timedelta, timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import User
from asgiref.sync import async_to_sync, sync_to_async
from videochat.models import Lobby


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
            print('connect')       
            self.lobby_code = self.scope["url_route"]["kwargs"]["lobby_code"]
            self.username = self.scope["url_route"]["kwargs"]["username"]
            
            lobby = await sync_to_async(Lobby.objects.filter(lobby_id=self.lobby_code).first)()
            print(lobby)
            if not lobby:
                await self.accept()
                print("send mess to fronted")
                # Room doesn't exist, send a custom message to the frontend
                await self.send(text_data=json.dumps({
                    'status' : 404,
                    'message': 'Room does not exist'
                }))
                await self.close()
                return
            
            user = await sync_to_async(User.objects.get)(username=self.username)
            
            await sync_to_async(lobby.lobby_users.add)(user)
            self.room_group_name = self.lobby_code
            
            print(self.username, self.lobby_code)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        self.lobby_code = self.scope["url_route"]["kwargs"]["lobby_code"]
        self.username = self.scope["url_route"]["kwargs"]["username"]
        
        print(self.lobby_code, self.username)

        # Wrap database operations with sync_to_async
        lobby = await sync_to_async(Lobby.objects.filter(lobby_id=self.lobby_code).first)()
        user = await sync_to_async(User.objects.filter(username=self.username).first)()
                 
        if lobby:
            await sync_to_async(lobby.lobby_users.remove)(user)
            bool1 = await sync_to_async(lobby.lobby_users.exists)()
            print(bool1)
            if not bool1:
                print('no users')
                print(lobby.created_at)
                current_datetime = datetime.now(timezone.utc)
                time_difference = current_datetime - lobby.created_at   
                if time_difference>timedelta(days=2):
                    print("hi")
                    # await sync_to_async(lobby.delete)()

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            
            print("Disconnected")
        else:
            print("no channel setuped so what to disconncet")

        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        print("/n")
        message = text_data_json["message"]
        action = text_data_json['action']
        if 'mapPeers' in message:
            peerObj = message['mapPeers']
            print(peerObj)
        else:
            peerObj = {}
        if action in ['new-offer', 'new-answer']:
            receiver_channel_name = text_data_json['message']['receiver_channel_name']  # Correct the key name here
            text_data_json['message']['receiver_channel_name'] = self.channel_name  # Correct the key name here
            await self.channel_layer.send(
                receiver_channel_name ,
                {
                    'type': 'send.sdp',
                    'message' : text_data_json,
                    "mapPeers" : peerObj
                }
            )
            return
            
        text_data_json['message']['receiver_channel_name'] = self.channel_name  # Correct the key name here

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'message' : text_data_json,
                "mapPeers" : peerObj
            }
        )




    async def send_sdp(self, event):
        # print(str(event['message'])+"<----")
        message = event['message']
        print(message)
        print("/n- answ")
        await self.send(text_data=json.dumps(message))