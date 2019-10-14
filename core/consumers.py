# core/consumers.py
import sys
import uuid
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import *

class CoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.commandsMapping = {
            'JOIN_CLIENT': self.onJoinClient,
            'JOIN_CAMERA': self.onJoinCamera,
            'CALL': self.onCall,
            'MESSAGE': self.onMessage,
        }

        self.identifier = "";

        await self.channel_layer.group_add('default', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('default', self.channel_name)
        await self.channel_layer.group_discard(self.identifier, self.channel_name)
        print('Disconnected: ' + self.identifier)
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        #print(data)
        try:
            await self.commandsMapping[data['command']](data)
        except Exception as err:
            print(type(err).__name__)
            print(err.args)
            await self.onError(err, data)

    async def onError(self, err, data):
        err_type = type(err).__name__
        err_message = str(err.args)
        print('Error: ' + err_type + ' => ' + err_message)
        await self.send(text_data=json.dumps({
            'command': 'SERVER_ERROR',
            'error': {
                'type': err_type,
                'message': err_message
                }
        }))

    async def onJoinClient(self, data):
        generated_uuid = uuid.uuid4().hex
        print('Client ' + generated_uuid + ' joined')
        self.identifier = generated_uuid
        await self.send(text_data=json.dumps({
            'command': 'JOINED_CLIENT',
            'identifier': generated_uuid
        }))

    async def onJoinCamera(self, data):
        ident = data['identifier']
        self.identifier = ident
        await self.channel_layer.group_add(self.identifier, self.channel_name)
        cam, created = Camera.objects.get_or_create(identifier=ident)
        print('Camera ' + cam.name + ': ' + cam.identifier + ' joined')
        await self.channel_layer.group_send('default', {
            'type': 'sendCameraUpdate',
            'message': {
                'command': 'UPDATE_CAMERAS',
                'identifier': cam.identifier
            }
        })
        await self.send(text_data=json.dumps({
            'command': 'JOINED_CAMERA'
        }))

    async def onCall(self, data):
        await self.channel_layer.group_send(data['identifier'], {
            'type': 'sendCall',
            'message': {
                'command': 'CALL',
                'identifier': self.identifier,
            }
        })

    async def onMessage(self, data):
        await self.channel_layer.group_send(data['identifier'], {
            'type': 'sendMessage',
            'message': {
                'command': 'MESSAGE',
                'identifier': self.identifier,
                'message': data['message']
            }
        })

    async def sendCall(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def sendMessage(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def sendCameraUpdate(self, event):
        await self.send(text_data=json.dumps(event['message']))