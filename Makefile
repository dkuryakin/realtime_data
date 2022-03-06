.PHONY: up down

up:
	docker-compose down
	docker-compose up --build --force-recreate --remove-orphans

down:
	docker-compose down