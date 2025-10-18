#!/bin/bash

echo "================================================"
echo "  Code Archaeology Explorer - Startup Script"
echo "================================================"
echo ""

echo "Starting Backend Server..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting Frontend Dev Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 2

echo ""
echo "================================================"
echo "  Servers Running!"
echo "================================================"
echo ""
echo "Backend API: http://localhost:5000"
echo "Frontend UI: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Open browser (works on macOS and Linux)
if command -v open &> /dev/null; then
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
fi

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
