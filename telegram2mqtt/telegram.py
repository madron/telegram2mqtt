import logging
import aiohttp


class TelegramBot:
    def __init__(self, token):
        self.logger = logging.getLogger('TelegramBot')
        self.token = token

    async def make_request(self, method_name, method='get', params=dict(), files=None, timeout=10):
        url = 'https://api.telegram.org/bot{token}/{method_name}'.format(token=self.token, method_name=method_name)
        self.logger.debug('make_request - {method} {method_name}'.format(method=method, method_name=method_name))

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get(url, params=params) as response:
                self.logger.debug('make_request - status code: {}'.format(response.status))
                assert response.status == 200
                data = await response.json()

        return data

    async def get_me(self):
        return await self.make_request(method_name='getMe')

    async def send_message(self, chat_id, text):
        params = dict(chat_id=str(chat_id), text=text)
        return await self.make_request(method_name='sendMessage', params=params)
