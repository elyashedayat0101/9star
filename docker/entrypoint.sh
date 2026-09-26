#!/bin/sh
set -e

wait_for_redis() {
    max_attempts=30
    attempt=1

    while true; do
        if python -c "
import os, sys, redis
url = os.environ.get('REDIS_URL') or os.environ.get('CELERY_BROKER_URL')
sys.exit(0) if not url else redis.from_url(url, socket_connect_timeout=3).ping()
" 2>/dev/null; then
            break
        fi

        if [ "$attempt" -ge "$max_attempts" ]; then
            echo "Redis did not become reachable after ${max_attempts} attempts - giving up." >&2
            exit 1
        fi

        echo "Waiting for Redis... (attempt ${attempt}/${max_attempts})"
        attempt=$((attempt + 1))
        sleep 2
    done
}

wait_for_redis

if [ "$1" = "gunicorn" ] || [ "$1" = "web" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

exec "$@"
