all:
	docker-compose up --build -d

clean:
	docker-compose down

fclean: clean
	docker-compose down -v
	docker system prune -af

purge.db:
	docker-compose down
	docker volume rm exercice4_postgres-data 2>/dev/null || true
	docker-compose up -d

purge.all: clean
	docker volume rm exercice4_postgres-data exercice4_pgadmin-data 2>/dev/null || true
	docker system prune -af --volumes
	rm -rf backend/src frontend/src 2>/dev/null || true

re: fclean all

.PHONY: all clean fclean purge.db purge.all re