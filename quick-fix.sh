#!/bin/bash

echo "🔧 ElderConnect Quick Fix Script"
echo "================================"
echo ""

# Stop all containers
echo "⏹️  Stopping all containers..."
docker-compose down -v

echo ""
echo "🧹 Cleaning up..."
sleep 2

echo ""
echo "🚀 Starting fresh with database initialization..."
docker-compose up --build

echo ""
echo "✅ Done! Your application should now be running."
echo ""
echo "Access points:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:5000"
echo "  Health:   http://localhost:5000/api/health"
