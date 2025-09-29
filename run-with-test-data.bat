@echo off
echo Starting PlayMetric with test data generation...

REM Build the application
call mvn clean package -DskipTests

REM Run the application with test data generation
java -jar target/playmetric-1.0-SNAPSHOT.jar --spring.profiles.active=data-load

echo Application is running. Access Swagger UI at http://localhost:8080/swagger-ui.html
