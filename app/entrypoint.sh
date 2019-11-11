#!/bin/sh

echo "Waiting for MySQL..."

if [ -z "$MYSQL_HOST" ]; then
    export MYSQL_HOST="127.0.0.1"
fi

if [ -z "$MYSQL_PORT" ]; then
    export MYSQL_PORT=3306
fi

while ! nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
    sleep 0.1
done

exec "$@"
