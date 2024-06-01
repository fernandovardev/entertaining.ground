@echo off
setlocal

:: Delete cache directories
echo Deleting cache directories...
for /d /r %%i in (__pycache__) do @if exist "%%i" rd /s /q "%%i"
if exist ".pytest_cache" rd /s /q ".pytest_cache"

:: Run tests using pytest
pytest
set TEST_EXIT_CODE=%ERRORLEVEL%

:: Check if tests passed
if %TEST_EXIT_CODE% equ 0 (
    echo Tests passed. Building and starting the application.

    :: Build and start the application using docker-compose.yml
    docker-compose up --build -d
) else (
    echo Tests failed. Exiting.
    exit /b 1
)

endlocal
