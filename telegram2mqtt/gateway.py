import logging
import os


logger = logging.getLogger()


class Gateway:
    def __init__(self, **kwargs):
        pass

    async def start(self):
        try:
            logger.info('Started')
        except:
            logger.exception('start')

    async def stop(self):
        try:
            logger.info('Stopped')
        except:
            logger.exception('stop')
