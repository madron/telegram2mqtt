import json
import unittest
import aiohttp
from aioresponses import aioresponses
from telegram2mqtt.telegram import TelegramBot


class TelegramBotTest(unittest.IsolatedAsyncioTestCase):
    async def test_make_request_get(self):
        bot = TelegramBot(token='token')
        with aioresponses() as mocked:
            body = '{"text": "test"}'
            mocked.get('https://api.telegram.org/bottoken/test_method', status=200, body=body)
            response = await bot.make_request(method='get', method_name='test_method')
            self.assertEqual(response, dict(text='test'))

    async def test_make_request_post(self):
        bot = TelegramBot(token='token')
        with aioresponses() as mocked:
            body = '{"text": "test"}'
            mocked.post('https://api.telegram.org/bottoken/test_method', status=200, body=body)
            response = await bot.make_request(method='post', method_name='test_method')
            self.assertEqual(response, dict(text='test'))

    async def test_make_request_wrong_method(self):
        bot = TelegramBot(token='token')
        with aioresponses() as mocked:
            body = '{"text": "test"}'
            mocked.get('https://api.telegram.org/bottoken/test_method', status=200, body=body)
            with self.assertRaises(AssertionError):
                await bot.make_request(method='patch', method_name='test_method')

    async def test_make_request_unauthorized(self):
        bot = TelegramBot(token='wrong')
        with aioresponses() as mocked:
            mocked.get('https://api.telegram.org/botwrong/test_method', status=401)
            with self.assertRaises(aiohttp.client_exceptions.ClientResponseError) as cm:
                await bot.make_request(method_name='test_method')
            self.assertEqual(cm.exception.status, 401)
            self.assertEqual(cm.exception.message, 'Unauthorized')

    async def test_make_request_wrong_method_name(self):
        bot = TelegramBot(token='token')
        with aioresponses() as mocked:
            mocked.get('https://api.telegram.org/bottoken/wrong_method', status=404)
            with self.assertRaises(aiohttp.client_exceptions.ClientResponseError) as cm:
                await bot.make_request(method_name='wrong_method')
            self.assertEqual(cm.exception.status, 404)
            self.assertEqual(cm.exception.message, 'Not Found')

    async def test_get_me(self):
        bot = TelegramBot(token='token')
        with aioresponses() as mocked:
            data = {'ok': True, 'result': {'id': 123456789, 'is_bot': True, 'first_name': 'TestBot', 'username': 'testbot', 'can_join_groups': True, 'can_read_all_group_messages': False, 'supports_inline_queries': False}}
            body = json.dumps(data)
            mocked.get('https://api.telegram.org/bottoken/getMe', status=200, body=body)
            response = await bot.get_me()
            self.assertEqual(response, data)

    async def test_send_message(self):
        bot = TelegramBot(token='token')
        with aioresponses() as mocked:
            data = {'ok': True, 'result': {'message_id': 123, 'from': {'id': 123456789, 'is_bot': True, 'first_name': 'TestBot', 'username': 'testbot'}, 'chat': {'id': 987654321, 'first_name': 'Joe', 'last_name': 'Black', 'type': 'private'}, 'date': 1607806841, 'text': 'test'}}
            body = json.dumps(data)
            mocked.get('https://api.telegram.org/bottoken/sendMessage?chat_id=987654321&text=test', status=200, body=body)
            response = await bot.send_message(chat_id=987654321, text='test')
            self.assertEqual(response, data)
