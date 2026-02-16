# Oscar Legal Practitioners - Development Setup Script for Windows
# This script automates the setup process

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Oscar Legal Practitioners - Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "WARNING: This is for educational purposes only" -ForegroundColor Yellow
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Green
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.1[1-9]|Python 3\.[2-9]") {
    Write-Host "✓ $pythonVersion detected" -ForegroundColor Green
} else {
    Write-Host "✗ Python 3.11+ required. Current: $pythonVersion" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check PostgreSQL
Write-Host "`nChecking PostgreSQL..." -ForegroundColor Green
try {
    $pgVersion = psql --version 2>&1
    Write-Host "✓ PostgreSQL found: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ PostgreSQL not found in PATH" -ForegroundColor Yellow
    Write-Host "Please install PostgreSQL 15+ from https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
}

# Create .env file
Write-Host "`nSetting up environment file..." -ForegroundColor Green
if (Test-Path ".env") {
    Write-Host "⚠ .env file already exists, skipping..." -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created from template" -ForegroundColor Green
    Write-Host "⚠ Please update .env with your actual configuration!" -ForegroundColor Yellow
}

# Setup Backend
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  Setting Up Backend" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if (Test-Path "backend\venv") {
    Write-Host "⚠ Backend virtual environment already exists" -ForegroundColor Yellow
} else {
    Write-Host "Creating backend virtual environment..." -ForegroundColor Green
    python -m venv backend\venv
    Write-Host "✓ Backend virtual environment created" -ForegroundColor Green
    
    Write-Host "Installing backend dependencies..." -ForegroundColor Green
    & backend\venv\Scripts\pip.exe install -r backend\requirements.txt
    Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
}

# Setup AI Service
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  Setting Up AI Service" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if (Test-Path "ai-service\venv") {
    Write-Host "⚠ AI service virtual environment already exists" -ForegroundColor Yellow
} else {
    Write-Host "Creating AI service virtual environment..." -ForegroundColor Green
    python -m venv ai-service\venv
    Write-Host "✓ AI service virtual environment created" -ForegroundColor Green
    
    Write-Host "Installing AI service dependencies (this may take a while)..." -ForegroundColor Green
    & ai-service\venv\Scripts\pip.exe install -r ai-service\requirements.txt
    Write-Host "✓ AI service dependencies installed" -ForegroundColor Green
}

# Create database
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  Database Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$createDb = Read-Host "Do you want to create the database now? (y/n)"
if ($createDb -eq "y") {
    $dbName = Read-Host "Enter database name (default: oscar_legal)"
    if ([string]::IsNullOrWhiteSpace($dbName)) {
        $dbName = "oscar_legal"
    }
    
    try {
        createdb $dbName
        Write-Host "✓ Database '$dbName' created successfully" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Database creation failed. It may already exist." -ForegroundColor Yellow
    }
}

# Next steps
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Configure Environment:" -ForegroundColor Yellow
Write-Host "   - Edit .env file with your configuration"
Write-Host "   - Add your OpenAI API key"
Write-Host "   - Update SECRET_KEY (generate with: python -c `"import secrets; print(secrets.token_urlsafe(32))`")"
Write-Host ""
Write-Host "2. Run Database Migrations:" -ForegroundColor Yellow
Write-Host "   cd backend"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   alembic upgrade head"
Write-Host ""
Write-Host "3. Start Development Servers:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Terminal 1 - Backend:" -ForegroundColor Cyan
Write-Host "   cd backend"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   uvicorn app.main:app --reload --port 8000"
Write-Host ""
Write-Host "   Terminal 2 - AI Service:" -ForegroundColor Cyan
Write-Host "   cd ai-service"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   uvicorn app.main:app --reload --port 8001"
Write-Host ""
Write-Host "   Terminal 3 - Frontend:" -ForegroundColor Cyan
Write-Host "   cd frontend"
Write-Host "   python -m http.server 3000"
Write-Host ""
Write-Host "4. Access the Application:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000"
Write-Host "   Backend API: http://localhost:8000/api/docs"
Write-Host "   AI Service: http://localhost:8001/api/docs"
Write-Host ""
Write-Host "For more information, see:" -ForegroundColor Green
Write-Host "   - README.md"
Write-Host "   - docs\QUICK_START.md"
Write-Host "   - IMPLEMENTATION_PLAN.md"
Write-Host ""
Write-Host "Happy Coding! 🎉" -ForegroundColor Green
