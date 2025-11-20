#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Running migrations..."
python manage.py migrate --no-input
python manage.py create_initial_manager

# Check the environment variable
if [ "$APP_ENV" = "production" ]; then
    echo "Collecting static files..."
    # This collects static files into STATIC_ROOT defined in settings.py
    python manage.py collectstatic --no-input --clear 
    
    echo "Starting Gunicorn..."
    # Start the production server using Gunicorn
    # Make sure 'app.wsgi:application' matches your project structure
    exec gunicorn app.wsgi:application --bind 0.0.0.0:8000
else
    echo "Starting Django development server..."
    # Start the development server (for local docker-compose)
    exec python manage.py runserver 0.0.0.0:8000
fi