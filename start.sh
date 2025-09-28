#!/bin/bash

# BillyBot Startup Script

echo "🤖 Starting BillyBot..."

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    exit 1
fi

# Check if required models are installed
echo "📋 Checking Ollama models..."
if ! ollama list | grep -q "nomic-embed-text"; then
    echo "📥 Pulling nomic-embed-text model..."
    ollama pull nomic-embed-text
fi

if ! ollama list | grep -q "llama3"; then
    echo "📥 Pulling llama3 model..."
    ollama pull llama3
fi

echo "✅ Ollama models ready"

# Start backend
echo "🚀 Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ BillyBot is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait

# Cleanup
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
