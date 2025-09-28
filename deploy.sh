#!/bin/bash

# BillyBot Deployment Script

echo "🚀 Deploying BillyBot..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ BillyBot is running!"
    echo "   Frontend: http://localhost"
    echo "   Backend API: http://localhost:8000"
    echo "   Ollama: http://localhost:11434"
    echo ""
    echo "📋 To stop the services:"
    echo "   docker-compose down"
    echo ""
    echo "📋 To view logs:"
    echo "   docker-compose logs -f"
else
    echo "❌ Failed to start services. Check logs:"
    docker-compose logs
    exit 1
fi
