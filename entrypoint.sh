#!/bin/bash
set -e

echo "Running migrations"
python manage.py migrate

# TODO: Should remove later
echo "Loading fixture data"
python manage.py loaddata core/fixtures/initial_data.json

echo "Starting server"
exec "$@"
