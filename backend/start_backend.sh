#!/bin/bash

# Start Backend Server Script
echo "================================"
echo "Starting Stride Backend Server"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 5

# Run data initialization
echo "Initializing database with sample data..."
python -c "from app.data_generator import seed_database; seed_database()"

# Start the server
echo "Starting FastAPI server..."
echo "Backend will be available at http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
python -m app.main
