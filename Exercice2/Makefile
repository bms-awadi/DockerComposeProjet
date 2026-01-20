all:
	docker-compose up --build -d

clean:
	docker-compose down

fclean: clean
	docker-compose down -v
	docker system prune -af

purge:
	docker-compose down -v
	docker volume rm exercice2_db-data 2>/dev/null || true
	docker-compose up --build -d

re: fclean all

.PHONY: all clean fclean purge re