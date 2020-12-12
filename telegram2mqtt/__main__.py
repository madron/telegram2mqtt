import argparse
import asyncio
import logging
from telegram2mqtt.gateway import Gateway


DEFAULT_LOGLEVEL = 'INFO'
LOGLEVEL_CHOICES = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
]


def main():
    # ArgumentParser
    parser = argparse.ArgumentParser(prog='telegram2mqtt', description='Telegram to Mqtt gateway')
    parser.add_argument('--loglevel', metavar='LEVEL', type=str,
                        default=DEFAULT_LOGLEVEL, choices=LOGLEVEL_CHOICES,
                        help="Log level. Default: '{}'".format(DEFAULT_LOGLEVEL))
    parser.add_argument('--debug', action='store_true')

    kwargs = vars(parser.parse_args())

    # Log config
    logging.basicConfig(level=kwargs['loglevel'], format='%(levelname)-8s %(message)s')

    logging.debug('Arguments')
    logging.debug('kwargs: {}'.format(kwargs))


    # Gateway
    gateway = Gateway(**kwargs)
    loop = asyncio.get_event_loop()
    loop.create_task(gateway.start())
    loop.run_forever()


if __name__ == '__main__':
    main()
