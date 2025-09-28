@echo off
echo 🚀 Deploying BillyBot...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Build and start services
echo 📦 Building and starting services...
docker-compose up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check if services are running
docker-compose ps | findstr "Up" >nul
if errorlevel 1 (
    echo ❌ Failed to start services. Check logs:
    docker-compose logs
    pause
    exit /b 1
) else (
    echo ✅ BillyBot is running!
    echo    Frontend: http://localhost
    echo    Backend API: http://localhost:8000
    echo    Ollama: http://localhost:11434
    echo.
    echo 📋 To stop the services:
    echo    docker-compose down
    echo.
    echo 📋 To view logs:
    echo    docker-compose logs -f
)

pause
