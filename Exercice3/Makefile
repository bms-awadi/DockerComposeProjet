all:
	docker-compose up --build -d

clean:
	docker-compose down

fclean: clean
	docker-compose down -v
	docker system prune -af

re: fclean all

.PHONY: all clean fclean re