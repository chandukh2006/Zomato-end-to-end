#!/bin/bash

# Bash script to start Zomato application with Docker

echo "🚀 Starting Zomato Application..."

# Check if .env.docker exists
if [ ! -f ".env.docker" ]; then
    echo "⚠️  .env.docker file not found!"
    echo "Creating .env.docker from example..."
    cp .env.docker.example .env.docker
    echo "✅ Please edit .env.docker and add your Google Maps API key!"
    read -p "Press Enter to continue after editing..."
fi

# Build images
echo ""
echo "📦 Building Docker images..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services!"
    exit 1
fi

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
echo ""
echo "📊 Checking service status..."
docker-compose ps

# Seed database
echo ""
echo "🌱 Seeding database..."
sleep 5
if curl -X POST http://localhost:8000/seed > /dev/null 2>&1; then
    echo "✅ Database seeded successfully!"
else
    echo "⚠️  Could not seed database automatically. Please seed manually:"
    echo "   curl -X POST http://localhost:8000/seed"
    echo "   Or visit http://localhost:8000/docs and use the /seed endpoint"
fi

echo ""
echo "✅ Application is running!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop:          docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
