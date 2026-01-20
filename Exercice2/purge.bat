@echo off
docker-compose down -v
docker volume rm exercice2_db-data 2>nul
docker-compose up --build -d