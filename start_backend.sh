#!/bin/bash
# Start Backend Server Script for Linux/WSL

echo "Starting Brain Tumor Detection Backend..."
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if model file exists
if [ ! -f "models/best_cnn.pth" ] && [ ! -f "best_cnn.pth" ]; then
    echo "Warning: Model file not found. Make sure best_cnn.pth exists."
fi

# Start backend
cd backend
echo "Starting server on http://0.0.0.0:8000"
echo "Press CTRL+C to stop"
echo ""
python main.py

