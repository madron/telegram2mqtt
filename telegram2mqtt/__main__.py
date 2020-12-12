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


def main():
    # ArgumentParser
    parser = argparse.ArgumentParser(prog='telegram2mqtt', description='Telegram to Mqtt gateway')
    parser.add_argument('-t', '--token', metavar='TOKEN', type=str,
                        default=TELEGRAM_API_TOKEN, help='Telegram api token. Default from TELEGRAM_API_TOKEN env var.')
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
