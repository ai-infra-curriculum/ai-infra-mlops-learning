#!/bin/bash
# Run model serving platform locally

set -e

echo "Starting Model Serving Platform..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "Loaded environment variables from .env"
fi

# Check if dependencies are installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if Docker services are running
if ! docker ps &> /dev/null; then
    echo "Warning: Docker is not running. Starting Docker Compose services..."
    docker-compose up -d postgres redis minio vault prometheus grafana
    echo "Waiting for services to be ready..."
    sleep 10
fi

# Run database migrations (TODO: implement)
# echo "Running database migrations..."
# alembic upgrade head

# Start the application
echo "Starting FastAPI server..."
echo "Server will be available at: http://localhost:${API_PORT:-8000}"
echo "API docs: http://localhost:${API_PORT:-8000}/docs"
echo ""

# Run with auto-reload for development
uvicorn src.api.server:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${API_PORT:-8000} \
    --reload \
    --log-level ${LOG_LEVEL:-info}
