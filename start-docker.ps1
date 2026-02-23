# PowerShell script to start Zomato application with Docker

Write-Host "🚀 Starting Zomato Application..." -ForegroundColor Green

# Check if .env.docker exists
if (-not (Test-Path ".env.docker")) {
    Write-Host "⚠️  .env.docker file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env.docker from example..." -ForegroundColor Yellow
    Copy-Item ".env.docker.example" ".env.docker"
    Write-Host "✅ Please edit .env.docker and add your Google Maps API key!" -ForegroundColor Yellow
    Write-Host "Press any key to continue after editing..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Build images
Write-Host "`n📦 Building Docker images..." -ForegroundColor Cyan
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

# Start services
Write-Host "`n🚀 Starting services..." -ForegroundColor Cyan
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services!" -ForegroundColor Red
    exit 1
}

# Wait for services to be ready
Write-Host "`n⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check status
Write-Host "`n📊 Checking service status..." -ForegroundColor Cyan
docker-compose ps

# Seed database
Write-Host "`n🌱 Seeding database..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/seed" -Method POST -UseBasicParsing
    Write-Host "✅ Database seeded successfully!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not seed database automatically. Please seed manually:" -ForegroundColor Yellow
    Write-Host "   curl -X POST http://localhost:8000/seed" -ForegroundColor Yellow
    Write-Host "   Or visit http://localhost:8000/docs and use the /seed endpoint" -ForegroundColor Yellow
}

Write-Host "`n✅ Application is running!" -ForegroundColor Green
Write-Host "`n📍 Access points:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "`n📝 Useful commands:" -ForegroundColor Cyan
Write-Host "   View logs:     docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop:          docker-compose down" -ForegroundColor White
Write-Host "   Restart:       docker-compose restart" -ForegroundColor White
Write-Host "`n"
