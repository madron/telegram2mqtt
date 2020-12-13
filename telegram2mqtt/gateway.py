import logging
from telegram2mqtt.mqtt import MqttManager
from telegram2mqtt.telegram import TelegramBot


class Gateway:
    def __init__(self, token=None, chat=dict(), **mqtt_parameters):
        self.logger = logging.getLogger('Gateway')
        self.bot = TelegramBot(token=token)
        self.mqtt = MqttManager(chat=chat, callback=self.mqtt_receive_message, **mqtt_parameters)
        self.chat = chat

    async def start(self):
        try:
            self.logger.info('Started')
            await self.mqtt.start()
        except:
            self.logger.exception('start')

    async def stop(self):
        try:
            await self.mqtt.stop()
            self.logger.info('Stopped')
        except:
            self.logger.exception('stop')

    async def mqtt_receive_message(self, chat_name, message):
        self.logger.debug('mqtt_receive_message {}: {}'.format(chat_name, message))
        chat_id = self.chat[chat_name]
        await self.bot.send_message(chat_id, message)
        self.logger.info('Sent message to {}'.format(chat_name))
