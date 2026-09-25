#!/bin/sh
set -e

# Run one-time setup only for the web process
if [ "$1" = "gunicorn" ] || [ "$1" = "web" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Hand off to the real command (from CMD or docker-compose command:)
exec "$@"