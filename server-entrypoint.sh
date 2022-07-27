#!/bin/sh

set -x

echo "sleep for 10 seconds to ensure db is up and ready"
sleep 10

echo "applying migrations..."
poetry run alembic upgrade head

echo "starting server..."
poetry run uvicorn streamrss.server.app:app --host 0.0.0.0 --port 8000