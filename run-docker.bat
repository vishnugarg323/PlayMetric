@echo off
echo Building and starting PlayMetric containers...

REM Stop any existing containers
docker-compose down

REM Remove old volumes to ensure fresh test data
docker volume rm playmetric_test_data playmetric_mongodb_data

REM Build and start the containers
docker-compose up --build

echo Application is starting. Once ready, access:
echo API Documentation: http://localhost:8080/swagger-ui.html
echo API Endpoints: http://localhost:8080/api/events
