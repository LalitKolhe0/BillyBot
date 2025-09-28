@echo off
echo 🤖 Starting BillyBot...

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama is not running. Please start Ollama first:
    echo    ollama serve
    pause
    exit /b 1
)

echo 📋 Checking Ollama models...
ollama list | findstr "nomic-embed-text" >nul
if errorlevel 1 (
    echo 📥 Pulling nomic-embed-text model...
    ollama pull nomic-embed-text
)

ollama list | findstr "llama3" >nul
if errorlevel 1 (
    echo 📥 Pulling llama3 model...
    ollama pull llama3
)

echo ✅ Ollama models ready

REM Start backend
echo 🚀 Starting backend server...
cd backend
start "Backend" cmd /k "python main.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo 🎨 Starting frontend server...
cd ..\frontend
start "Frontend" cmd /k "npm start"

echo ✅ BillyBot is running!
echo    Frontend: http://localhost:3000
echo    Backend: http://localhost:8000
echo.
echo Press any key to exit...
pause >nul
