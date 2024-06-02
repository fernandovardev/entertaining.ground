@echo off

:: Run tests with pytest
pytest --disable-warnings --maxfail=1
if %errorlevel% neq 0 (
    echo Tests failed, exiting.
    exit /b 1
)

:: Build and start Docker containers
docker-compose up --build
