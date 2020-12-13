import asyncio
import logging
from contextlib import AsyncExitStack
from asyncio_mqtt import Client, Will


class MqttManager:
    def __init__(
        self,
        chat=dict(),
        hostname='localhost',
        port=1883,
        username=None,
        password=None,
        prefix='telegram',
        callback=None,
    ):
        self.logger = logging.getLogger('MqttManager')
        self.chat = chat
        self.callback = callback
        self.status_topic = '{}/status'.format(prefix)
        will = Will(self.status_topic, payload='offline', qos=1, retain=True)
        self.client = Client(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            will=will,
        )
        self.prefix = prefix
        self.chat_topics = ['{}/send/{}'.format(self.prefix, name) for name in self.chat.keys()]
        self.listen_task = None

    async def start(self):
        try:
            self.logger.info('Started')
            await self.connect()
        except:
            self.logger.exception('start')

    async def stop(self):
        try:
            await self.disconnect()
            self.logger.info('Stopped')
        except:
            self.logger.exception('stop')

    async def connect(self):
        await self.client.connect()
        await self.client.publish(self.status_topic, 'online', qos=1)
        self.task = asyncio.create_task(self.listen())
        self.logger.info('Connected')

    async def disconnect(self):
        await self.client.unsubscribe(*self.chat_topics)
        await self.client.publish(self.status_topic, 'offline', qos=1)
        await self.client.disconnect()
        self.logger.info('Disconnected')

    async def listen(self):
        try:
            filter_topic = '{}/send/#'.format(self.prefix)
            async with self.client.filtered_messages(filter_topic) as messages:
                await self.client.subscribe(*self.chat_topics)
                async for message in messages:
                    payload = message.payload.decode()
                    self.logger.debug('Message received. {}: {}'.format(message.topic, payload))
                    if self.callback:
                        name = message.topic.replace('{}/send/'.format(self.prefix), '', 1)
                        await self.callback(name, payload)
        except:
            self.logger.exception('listen')
