#!/bin/sh
set -e

echo "Creating migrations..."
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec "$@"
