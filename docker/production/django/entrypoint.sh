#!/usr/bin/env sh
set -e

# Optional: wait for DB if provided
if [ -n "$WAIT_FOR_DB_HOST" ] && [ -n "$WAIT_FOR_DB_PORT" ]; then
  /wait-for-it.sh "$WAIT_FOR_DB_HOST:$WAIT_FOR_DB_PORT" -t 30
fi

# Optional: migrations/static
[ "${DJANGO_MIGRATE:-1}" = "1" ] && python manage.py migrate --noinput
[ "${DJANGO_COLLECTSTATIC:-0}" = "1" ] && python manage.py collectstatic --noinput

# Hand off to the main process (from CMD or docker-compose command)
exec "$@"