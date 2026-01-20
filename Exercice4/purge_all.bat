@echo off
docker-compose down
docker volume rm exercice4_postgres-data exercice4_pgadmin-data 2>nul
docker system prune -af --volumes
rmdir /s /q backend\src 2>nul
rmdir /s /q frontend\src 2>nul