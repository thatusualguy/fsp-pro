# entrypoint.sh
#!/bin/sh
set -e
echo "Collecting static files…"
python manage.py collectstatic --noinput
echo "Starting server…"
exec gunicorn src.wsgi:application --bind 0.0.0.0:9090
