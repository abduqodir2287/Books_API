#!/bin/sh

echo "Выполняем миграции..."
python manage.py migrate --noinput

echo "Собираем статику..."
python manage.py collectstatic --noinput

exec "$@"
