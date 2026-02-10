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

  # Compile assets only if not present (speeds up restart)
  if [ ! -d "/app/data/collected_static/admin" ]; then
      echo "Compiling assets (this may take a while)..."
      ./make_style.sh
      python manage.py collectstatic --no-input
      python manage.py compilemessages
      python manage.py compilejsi18n
      python manage.py compress
  else
      echo "Assets already compiled, skipping..."
  fi
  
  # Always ensure compression manifest exists
  if [ ! -f "/app/data/collected_static/CACHE/manifest.json" ]; then
      echo "Compression manifest missing, running compress..."
      python manage.py compress
  fi
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
