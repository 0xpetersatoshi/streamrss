#!/bin/sh

set -x

echo "starting feed fetching worker..."
poetry install
poetry run python streamrss/feeds/__init__.py