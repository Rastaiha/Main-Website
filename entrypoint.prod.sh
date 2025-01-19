#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting the entrypoint script..."

if [ "$DATABASE" = "postgres" ]; then
    echo "Configured database is PostgreSQL. Waiting for PostgreSQL to be ready..."

    # Check PostgreSQL readiness
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done

    echo "PostgreSQL is up - continuing..."
fi

echo "Running database migrations..."
python3 manage.py migrate --no-input
echo "Database migrations completed."

echo "Collecting static files..."
python3 manage.py collectstatic --no-input --clear
echo "Static files collected."

echo "Starting the application..."
exec "$@"  # Execute the command passed to the script (e.g., gunicorn or Django's runserver)
