# Multi-stage build for BillyBot
FROM node:18-alpine AS frontend-build

# Set working directory
WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY frontend/ ./

# Build the React app
RUN npm run build

# Python backend stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./

# Copy built frontend
COPY --from=frontend-build /app/frontend/build ./static

# Create a simple HTTP server for the frontend
RUN pip install fastapi[all] uvicorn

# Create a simple static file server
RUN echo 'from fastapi import FastAPI\nfrom fastapi.staticfiles import StaticFiles\nfrom fastapi.responses import FileResponse\nimport os\n\napp = FastAPI()\napp.mount("/static", StaticFiles(directory="static"), name="static")\n\n@app.get("/")\ndef read_root():\n    return FileResponse("static/index.html")\n\nif __name__ == "__main__":\n    import uvicorn\n    uvicorn.run(app, host="0.0.0.0", port=8000)' > static_server.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "main.py"]
