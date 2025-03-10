#!/bin/bash

# Start backend server in the background
echo "Starting backend server..."
python chatbot/backend/main.py &

# Wait a few seconds for backend to initialize
echo "Waiting for backend to initialize..."
sleep 5

# Navigate to frontend directory and start React app
echo "Starting frontend application..."
cd chatbot/frontend
npm start
