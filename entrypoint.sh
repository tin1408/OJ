#!/bin/bash
set -e

# Wait for DB
echo "Waiting for database..."
while ! nc -z vnoi-db 3306; do
  sleep 1
done
echo "Database is up!"

# Run initialization steps only if INIT_VNOJ is true
if [ "$INIT_VNOJ" = "true" ]; then
  # Run migrations
  python manage.py migrate

  # Load initial data
  python manage.py loaddata navbar
  python manage.py loaddata language_small
  python manage.py shell < init_data.py

  # Compile assets
  ./make_style.sh
  python manage.py collectstatic --no-input
  python manage.py compilemessages
  python manage.py compilejsi18n
else
  # Still good to wait for a bit to let vnoi-web finish if it's running
  echo "Skipping initialization, waiting for vnoi-web..."
  sleep 10
fi

# Start server or command
if [ $# -gt 0 ]; then
  exec "$@"
else
  exec python manage.py runserver 0.0.0.0:8000
fi
