FROM python:3.10

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry install --no-dev

COPY alembic.ini ./
COPY alembic ./alembic
COPY Makefile ./
COPY .env ./
COPY entrypoint.sh ./
COPY streamrss/ ./streamrss

ENTRYPOINT [ "./entrypoint.sh" ]