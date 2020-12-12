import logging
from telegram2mqtt.telegram import TelegramBot


class Gateway:
    def __init__(self, token=None):
        self.logger = logging.getLogger('Gateway')
        self.bot = TelegramBot(token=token)

    async def start(self):
        try:
            self.logger.info('Started')
        except:
            self.logger.exception('start')

    async def stop(self):
        try:
            self.logger.info('Stopped')
        except:
            self.logger.exception('stop')
