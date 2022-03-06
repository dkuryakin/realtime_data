.PHONY: up down

up:
	docker-compose up --build --force-recreate --remove-orphans

down:
	docker-compose down