#!/bin/bash

# Start Frontend Server Script
echo "================================"
echo "Starting Stride Frontend Server"
echo "================================"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the development server
echo "Starting Vite development server..."
echo "Frontend will be available at http://localhost:5173"
npm run dev
