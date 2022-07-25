install:
	@poetry install

start-db:
	@docker-compose up -d

run-migrations:
	@poetry run alembic upgrade head

start-server: start-db run-migrations
	@poetry run uvicorn streamrss.server.app:app --reload

destroy:
	@docker-compose down --remove-orphans
	@docker volume rm $$(docker volume ls --filter label=com.docker.compose.volume=streamrss | sed '1d' | awk '{print $$2}')