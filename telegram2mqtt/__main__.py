import argparse
import asyncio
import logging
import os
from telegram2mqtt.gateway import Gateway


DEFAULT_LOGLEVEL = 'INFO'
LOGLEVEL_CHOICES = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
]
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', None)

class StoreDict(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         kwargs = {}
         for kv in values.split(','):
             k, v = kv.split('=')
             kwargs[k] = v
         setattr(namespace, self.dest, kwargs)


def main():
    # ArgumentParser
    parser = argparse.ArgumentParser(prog='telegram2mqtt', description='Telegram to Mqtt gateway')
    parser.add_argument('-t', '--token', metavar='TOKEN', type=str,
                        default=TELEGRAM_API_TOKEN, help='Telegram api token. Default from TELEGRAM_API_TOKEN env var.')
    parser.add_argument('--hostname', metavar='HOST', type=str, default='localhost')
    parser.add_argument('--port', metavar='PORT', type=int, default=1883)
    parser.add_argument('--username', metavar='USER', type=str)
    parser.add_argument('--password', metavar='PASS', type=str)
    parser.add_argument('--prefix', metavar='PASS', type=str, default='telegram')
    parser.add_argument('--chat', action=StoreDict, metavar="name=id,name=id...")
    parser.add_argument('--loglevel', metavar='LEVEL', type=str,
                        default=DEFAULT_LOGLEVEL, choices=LOGLEVEL_CHOICES,
                        help="Log level. Default: '{}'".format(DEFAULT_LOGLEVEL))

    kwargs = vars(parser.parse_args())
    if not kwargs['token']:
        exit(parser.print_usage())

    # Log config
    loglevel = kwargs.pop('loglevel')
    logging.basicConfig(level=loglevel, format=' %(levelname)-8s %(name)s %(message)s')

    # Gateway
    gateway = Gateway(**kwargs)
    loop = asyncio.get_event_loop()
    loop.create_task(gateway.start())
    loop.run_forever()


if __name__ == '__main__':
    main()
