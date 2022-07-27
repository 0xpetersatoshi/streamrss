#!/bin/sh

set -x

echo "applying migrations..."
poetry run alembic upgrade head

echo "starting server..."
poetry run uvicorn streamrss.server.app:app --host 0.0.0.0 --port 8000