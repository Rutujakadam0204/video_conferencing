# clients are gonna connect to our websockets and will connect through this consumers
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.dispatch.dispatcher import receiver


class ChatConsumer(AsyncWebsocketConsumer):

    # will be triggered whenever a client connects to consumer
    async def connect(self):  
        self.room_group_name = 'Test_Room'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # will be triggered whenever a client disconnects to consumer
    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('Disconnected')

    # whenever a msg is received from a client
    async def receive(self, text_data):
        #most of the code for sending sdp and notifying every peer wnenevr sent sdp
        #receive code from js in dict format or json so deserialize json
        receive_dict = json.loads(text_data)
        message = receive_dict['message']
        action = receive_dict['action']

        if (action == 'new-pffer') or (action == 'new-answer'):
            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            receive_dict['message']['receiver_channel_name'] = self.channel_name
            await self.channel_layer.send(
            receiver_channel_name,
            {
                'type': 'send.sdp',
                'receive_dict':receive_dict
            }
            )
            return

        receive_dict['message']['receiver_channel_name'] = self.channel_name
        
        #send msg to all the other peers
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_dict':receive_dict
            }
        )

    async def send_sdp(self, event):
        receive_dict = event['receive_dict']

        #send msg to other peer
        await self.send(text_data=json.dumps(receive_dict))

        #dumps bcz converting from python to json
