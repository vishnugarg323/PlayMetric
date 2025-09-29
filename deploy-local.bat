@echo off
echo Setting up PlayMetric local development environment...

REM Create deployment directory if it doesn't exist
mkdir deployment 2>nul

REM Stop any running containers and clean up
docker-compose down
docker volume rm playmetric_mongodb_data playmetric_mongodb_analytics_data 2>nul

REM Build and start the services
docker-compose up --build

echo Local development environment is ready:
echo Main Service: http://localhost:8080
echo API Documentation: http://localhost:8080/swagger-ui.html
echo MongoDB Main: localhost:27017
echo MongoDB Analytics: localhost:27018
