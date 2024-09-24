#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 5
done

echo "PostgreSQL started"

exec "$@"