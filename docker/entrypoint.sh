#!/bin/sh
set -e

if [ "$1" = 'telegram2mqtt' ]; then
    exec su-exec nobody telegram2mqtt ${@:13}
else
    exec "$@"
fi
