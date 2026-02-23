.PHONY: help docker-build docker-up docker-down docker-logs docker-seed docker-clean

help:
	@echo "Available commands:"
	@echo "  make docker-build    - Build Docker images"
	@echo "  make docker-up      - Start all services"
	@echo "  make docker-down    - Stop all services"
	@echo "  make docker-logs     - View logs"
	@echo "  make docker-seed     - Seed the database"
	@echo "  make docker-clean    - Stop and remove volumes"

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-seed:
	@echo "Seeding database..."
	curl -X POST http://localhost:8000/seed || docker exec zomato-backend curl -X POST http://localhost:8000/seed

docker-clean:
	docker-compose down -v

docker-restart:
	docker-compose restart

docker-ps:
	docker-compose ps
