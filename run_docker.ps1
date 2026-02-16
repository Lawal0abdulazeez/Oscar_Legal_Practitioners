# run_docker.ps1 - Automated Docker Setup Script for Oscar Legal Practitioners

Write-Host "🚀 Starting Oscar Legal Practitioners System (Docker Mode)..." -ForegroundColor Cyan

# Check for Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed or not in PATH. Please install Docker first." -ForegroundColor Red
    exit 1
}

# Check for .env file
if (-not (Test-Path .env)) {
    Write-Host "⚠️ .env file not found. Creating from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file. Please edit it with your API keys if needed." -ForegroundColor Green
} else {
    Write-Host "✅ .env file found." -ForegroundColor Green
}

# Build and start containers
Write-Host "🐳 Building and starting containers (this may take a few minutes)..." -ForegroundColor Cyan
try {
    docker-compose up --build -d
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose failed."
    }
    Write-Host "✅ Containers started successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start containers. Please check Docker logs." -ForegroundColor Red
    exit 1
}

# Show running services
Write-Host "`n📊 Running Services:" -ForegroundColor Cyan
docker-compose ps

Write-Host "`n🌐 Access Points:" -ForegroundColor Cyan
Write-Host "   Frontend:    http://localhost:80"
Write-Host "   Backend API: http://localhost:8000/docs"
Write-Host "   AI Service:  http://localhost:8001/docs"
Write-Host "   Database:    localhost:5432"
Write-Host "   Redis:       localhost:6379"

Write-Host "`n📝 To stop services, run: docker-compose down" -ForegroundColor Yellow
Write-Host "Happy coding! 🚀" -ForegroundColor Cyan
