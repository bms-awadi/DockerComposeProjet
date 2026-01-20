@echo off
docker-compose down
docker volume rm exercice4_postgres-data 2>nul
docker-compose up -d