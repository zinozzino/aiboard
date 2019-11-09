#!/bin/sh

if [ -z "$PGHOST" ]; then
  export PGHOST="host.docker.internal"
fi

if [ -z "$PGPORT" ]; then
  export PGPORT="5432"
fi

while ! nc -z "$PGHOST" "$PGPORT" 2>/dev/null ; do
  sleep 0.1
done

exec "dumb-init" "--" "$@"
