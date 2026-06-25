#!/bin/sh
set -e

echo "Waiting for database to be ready..."

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres at $SQL_HOST:$SQL_PORT..."

    until nc -z "$SQL_HOST" "$SQL_PORT" 2>/dev/null; do
        echo "Postgres not ready yet..."
        sleep 1
    done

    echo "PostgreSQL started"
fi

echo "Running migrations..."
alembic -c /app/src/alembic.ini upgrade head

exec "$@"