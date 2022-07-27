install: create-env-file start-services
	@poetry install

start-services:
	@docker-compose up -d --build

create-env-file:
	@cp .env.example .env

run-migrations:
	@poetry run alembic upgrade head

start-server: start-services run-migrations
	@poetry run uvicorn streamrss.server.app:app --reload

destroy:
	@docker-compose down --remove-orphans
	@docker volume rm $$(docker volume ls --filter label=com.docker.compose.volume=streamrss | sed '1d' | awk '{print $$2}')