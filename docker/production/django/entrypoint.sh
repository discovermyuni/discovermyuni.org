#!/bin/sh

set -o errexit

. /venv/bin/activate

/wait-for-it.sh "$POSTGRES_HOST:$POSTGRES_PORT" -- echo "PostgreSQL is up - executing command"

exec "$@"

