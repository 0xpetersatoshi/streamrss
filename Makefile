run_migrations:
	@poetry run alembic upgrade head

start_server:
	@poetry run uvicorn streamrss.server.app:app --reload