@echo off
setlocal enabledelayedexpansion

echo PlayMetric Deployment Script
echo 1. Run main service only
echo 2. Run main service with test data generator
choice /C 12 /M "Select an option:"

if errorlevel 2 (
    echo Starting PlayMetric with test data generator...
    docker-compose up --build
) else (
    echo Starting PlayMetric main service only...
    docker-compose up --build playmetric-service mongodb mongodb-analytics
)

endlocal
