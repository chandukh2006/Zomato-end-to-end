# Docker Setup - Step by Step Guide

This guide will walk you through building Docker images and running the entire Zomato application.

## Prerequisites

- Docker Desktop installed (Windows/Mac) or Docker Engine + Docker Compose (Linux)
- Google Maps API Key (get it from [Google Cloud Console](https://console.cloud.google.com/))

## Step-by-Step Instructions

### Step 1: Navigate to Project Directory

```bash
cd c:\Users\khcha\OneDrive\Desktop\zomato
```

### Step 2: Create Environment File

Create a `.env.docker` file in the root directory:

**Windows (PowerShell):**
```powershell
Copy-Item .env.docker.example .env.docker
```

**Linux/Mac:**
```bash
cp .env.docker.example .env.docker
```

### Step 3: Edit Environment Variables

Open `.env.docker` file and add your Google Maps API key:

```env
# Backend
SECRET_KEY=your-secret-key-minimum-32-chars-change-in-production-12345
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Important:** Replace `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` with your actual Google Maps API key.

### Step 4: Build Docker Images

Build all Docker images (this may take 5-10 minutes the first time):

```bash
docker-compose build
```

**Or build specific services:**
```bash
# Build backend only
docker-compose build backend

# Build frontend only
docker-compose build frontend

# Build MongoDB (uses pre-built image, no build needed)
```

### Step 5: Start All Services

Start all containers:

```bash
docker-compose up -d
```

The `-d` flag runs containers in detached mode (background).

**To see logs while starting:**
```bash
docker-compose up
```

### Step 6: Verify Services Are Running

Check if all containers are running:

```bash
docker-compose ps
```

You should see:
- `zomato-mongodb` - Running
- `zomato-backend` - Running  
- `zomato-frontend` - Running

### Step 7: Seed the Database

Populate the database with sample restaurants and menu items:

**Option 1: Using curl (if available):**
```bash
curl -X POST http://localhost:8000/seed
```

**Option 2: Using PowerShell (Windows):**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/seed -Method POST
```

**Option 3: Using Docker exec:**
```bash
docker exec zomato-backend curl -X POST http://localhost:8000/seed
```

**Option 4: Using browser:**
- Open http://localhost:8000/docs
- Find the `/seed` endpoint
- Click "Try it out" → "Execute"

### Step 8: Access the Application

Open your browser and visit:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Quick Commands Reference

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

### Stop and Remove Volumes (⚠️ Deletes Database)

```bash
docker-compose down -v
```

### Restart Services

```bash
docker-compose restart

# Or restart specific service
docker-compose restart backend
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up --build -d

# Rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

### Check Container Status

```bash
docker-compose ps
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

## Troubleshooting

### Port Already in Use

If ports 3000, 8000, or 27017 are already in use:

1. **Find what's using the port:**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

2. **Stop the conflicting service**, or

3. **Change ports in docker-compose.yml:**
   ```yaml
   ports:
     - "8001:8000"  # Change host port
   ```

### Build Failures

```bash
# Clear Docker cache and rebuild
docker system prune -a
docker-compose build --no-cache
```

### MongoDB Connection Issues

```bash
# Check MongoDB logs
docker-compose logs mongodb

# Verify MongoDB is running
docker exec zomato-mongodb mongosh --eval "db.adminCommand('ping')"
```

### Frontend Can't Connect to Backend

1. Verify backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Test backend directly: `curl http://localhost:8000/`

### Environment Variables Not Loading

1. Ensure `.env.docker` exists in root directory
2. Check variable names match docker-compose.yml
3. Restart containers: `docker-compose restart`

## Production Deployment

For production, use the production compose file:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

**Important:** Update `.env.docker` with production values before running.

## Complete Example Workflow

```bash
# 1. Navigate to project
cd c:\Users\khcha\OneDrive\Desktop\zomato

# 2. Create env file
cp .env.docker.example .env.docker
# Edit .env.docker with your API keys

# 3. Build images
docker-compose build

# 4. Start services
docker-compose up -d

# 5. Wait for services to be ready (30 seconds)
# Check status
docker-compose ps

# 6. Seed database
curl -X POST http://localhost:8000/seed

# 7. Open browser
# Visit http://localhost:3000
```

## Using Makefile (Optional)

If you have `make` installed, you can use:

```bash
make docker-build    # Build images
make docker-up       # Start services
make docker-down     # Stop services
make docker-logs     # View logs
make docker-seed      # Seed database
make docker-clean     # Stop and remove volumes
```

## Next Steps

After containers are running:

1. ✅ Seed the database (Step 7)
2. ✅ Open http://localhost:3000
3. ✅ Register a new account
4. ✅ Browse restaurants
5. ✅ Add items to cart
6. ✅ Place an order

## Need Help?

- Check logs: `docker-compose logs -f`
- Verify containers: `docker-compose ps`
- Test API: http://localhost:8000/docs
- Check Docker Desktop dashboard (if using Docker Desktop)
