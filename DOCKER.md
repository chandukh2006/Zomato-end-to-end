# Docker Setup Guide

This guide explains how to run the Zomato application using Docker and Docker Compose.

## Prerequisites

- Docker Desktop installed (or Docker Engine + Docker Compose)
- Docker version 20.10+
- Docker Compose version 2.0+

## Quick Start

### 1. Clone/Download the Project

Make sure you have all the project files in the `zomato` directory.

### 2. Set Up Environment Variables

Create a `.env.docker` file in the root directory:

```bash
cp .env.docker.example .env.docker
```

Edit `.env.docker` and fill in your values:
```env
SECRET_KEY=your-secret-key-minimum-32-chars-change-in-production
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_KEY=your-google-maps-api-key
```

### 3. Build and Run (Development Mode)

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

This will:
- Start MongoDB on port 27017
- Start Backend API on port 8000
- Start Frontend on port 3000

### 4. Seed the Database

Once all containers are running, seed the database:

```bash
# Using curl
curl -X POST http://localhost:8000/seed

# Or using docker exec
docker exec zomato-backend curl -X POST http://localhost:8000/seed
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

## Production Deployment

For production, use the production compose file:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

**Note**: Update environment variables in `.env.docker` before running in production.

## Docker Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes (⚠️ This deletes MongoDB data)
```bash
docker-compose down -v
```

### Rebuild After Code Changes
```bash
# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Rebuild and restart
docker-compose up --build
```

### Execute Commands in Containers
```bash
# Backend shell
docker exec -it zomato-backend /bin/bash

# Frontend shell
docker exec -it zomato-frontend /bin/sh

# MongoDB shell
docker exec -it zomato-mongodb mongosh
```

### Check Container Status
```bash
docker-compose ps
```

## Individual Service Commands

### Build Backend Only
```bash
cd backend
docker build -t zomato-backend .
docker run -p 8000:8000 --env-file ../.env.docker zomato-backend
```

### Build Frontend Only
```bash
cd frontend
docker build -t zomato-frontend .
docker run -p 3000:3000 --env-file ../.env.docker zomato-frontend
```

## Troubleshooting

### Port Already in Use
If ports 3000, 8000, or 27017 are already in use:

1. Stop the conflicting service, or
2. Modify ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change host port
```

### MongoDB Connection Issues
- Ensure MongoDB container is running: `docker-compose ps`
- Check MongoDB logs: `docker-compose logs mongodb`
- Verify connection string in backend environment

### Frontend Can't Connect to Backend
- In development, use `http://localhost:8000`
- In Docker, backend service name is `backend`, so use `http://backend:8000` for internal communication
- Frontend should use `http://localhost:8000` for browser requests

### Build Failures
- Clear Docker cache: `docker system prune -a`
- Rebuild without cache: `docker-compose build --no-cache`

### Environment Variables Not Loading
- Ensure `.env.docker` file exists in root directory
- Check variable names match those in `docker-compose.yml`
- Restart containers after changing `.env.docker`

## Volume Persistence

MongoDB data is persisted in a Docker volume named `mongodb_data`. To backup:

```bash
# Create backup
docker exec zomato-mongodb mongodump --out /data/backup

# Copy backup from container
docker cp zomato-mongodb:/data/backup ./backup
```

## Health Checks

Production compose file includes health checks. View health status:

```bash
docker-compose ps
```

## Clean Up

Remove everything (containers, volumes, networks):

```bash
docker-compose down -v --remove-orphans
docker system prune -a
```

## Development vs Production

### Development (`docker-compose.yml`)
- Hot reload enabled for backend
- Development builds
- Volume mounts for live code updates

### Production (`docker-compose.prod.yml`)
- Optimized builds
- Health checks
- No volume mounts (uses built images)
- Restart policies set to `always`

## Security Notes

1. **Never commit `.env.docker`** - It contains sensitive keys
2. **Change SECRET_KEY** - Use a strong random string in production
3. **Use secrets management** - For production, consider Docker secrets or external secret managers
4. **Network isolation** - Services communicate via internal Docker network

## Next Steps

After containers are running:
1. Seed the database (see step 4 above)
2. Register a user account
3. Browse restaurants and place orders!
