"""
Oscar Legal Practitioners - Project Setup Script
This script helps set up the development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is 3.11 or higher"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_error(f"Python 3.11+ required. Current version: {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_postgresql():
    """Check if PostgreSQL is installed"""
    print_info("Checking PostgreSQL installation...")
    try:
        result = subprocess.run(['psql', '--version'], 
                              capture_output=True, text=True, check=True)
        print_success(f"PostgreSQL found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("PostgreSQL not found or not in PATH")
        print_info("Please install PostgreSQL 15+ from: https://www.postgresql.org/download/")
        return False

def create_directory_structure():
    """Create necessary directories"""
    print_info("Creating directory structure...")
    
    directories = [
        "backend/app/api/v1",
        "backend/app/core",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/services",
        "backend/app/utils",
        "backend/alembic/versions",
        "backend/tests",
        "backend/logs",
        "ai-service/app/api/v1",
        "ai-service/app/core",
        "ai-service/app/services",
        "ai-service/app/rag",
        "ai-service/app/utils",
        "ai-service/data/vector_db",
        "ai-service/data/templates",
        "ai-service/data/knowledge_base",
        "ai-service/tests",
        "ai-service/logs",
        "frontend/public",
        "frontend/assets/css",
        "frontend/assets/js",
        "frontend/assets/images",
        "frontend/components",
        "scripts",
        "docs",
        "docker",
        "shared",
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py for Python packages
        if 'app' in directory or directory.startswith('shared'):
            init_file = path / '__init__.py'
            if not init_file.exists():
                init_file.touch()
    
    print_success("Directory structure created")

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    print_info("Setting up environment file...")
    
    if Path('.env').exists():
        print_warning(".env file already exists, skipping...")
        return
    
    if Path('.env.example').exists():
        shutil.copy('.env.example', '.env')
        print_success(".env file created from .env.example")
        print_warning("Please update .env with your actual configuration!")
    else:
        print_error(".env.example not found")

def setup_backend_venv():
    """Set up backend virtual environment"""
    print_info("Setting up backend virtual environment...")
    
    backend_venv = Path('backend/venv')
    
    if backend_venv.exists():
        print_warning("Backend venv already exists, skipping...")
        return True
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', str(backend_venv)], 
                      check=True)
        print_success("Backend virtual environment created")
        
        # Determine pip path based on OS
        if sys.platform == 'win32':
            pip_path = backend_venv / 'Scripts' / 'pip.exe'
        else:
            pip_path = backend_venv / 'bin' / 'pip'
        
        print_info("Installing backend dependencies...")
        subprocess.run([str(pip_path), 'install', '-r', 'backend/requirements.txt'], 
                      check=True)
        print_success("Backend dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set up backend environment: {e}")
        return False

def setup_ai_venv():
    """Set up AI service virtual environment"""
    print_info("Setting up AI service virtual environment...")
    
    ai_venv = Path('ai-service/venv')
    
    if ai_venv.exists():
        print_warning("AI service venv already exists, skipping...")
        return True
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', str(ai_venv)], 
                      check=True)
        print_success("AI service virtual environment created")
        
        # Determine pip path based on OS
        if sys.platform == 'win32':
            pip_path = ai_venv / 'Scripts' / 'pip.exe'
        else:
            pip_path = ai_venv / 'bin' / 'pip'
        
        print_info("Installing AI service dependencies (this may take a while)...")
        subprocess.run([str(pip_path), 'install', '-r', 'ai-service/requirements.txt'], 
                      check=True)
        print_success("AI service dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set up AI service environment: {e}")
        return False

def create_database():
    """Create PostgreSQL database"""
    print_info("Creating PostgreSQL database...")
    
    response = input("Do you want to create the database now? (y/n): ")
    if response.lower() != 'y':
        print_warning("Skipping database creation")
        return
    
    db_name = input("Enter database name (default: oscar_legal): ").strip() or "oscar_legal"
    
    try:
        subprocess.run(['createdb', db_name], check=True)
        print_success(f"Database '{db_name}' created successfully")
    except subprocess.CalledProcessError:
        print_warning(f"Database '{db_name}' may already exist or createdb failed")
    except FileNotFoundError:
        print_error("createdb command not found. Please create database manually")

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print(f"{Colors.OKGREEN}Next Steps:{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}1. Configure Environment:{Colors.ENDC}")
    print(f"   Edit .env file with your configuration")
    print(f"   - Add your database URL")
    print(f"   - Add your OpenAI API key")
    print(f"   - Update SECRET_KEY\n")
    
    print(f"{Colors.BOLD}2. Run Database Migrations:{Colors.ENDC}")
    print(f"   cd backend")
    if sys.platform == 'win32':
        print(f"   venv\\Scripts\\activate")
    else:
        print(f"   source venv/bin/activate")
    print(f"   alembic upgrade head\n")
    
    print(f"{Colors.BOLD}3. Start Development Servers:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}Terminal 1 - Backend:{Colors.ENDC}")
    print(f"   cd backend")
    if sys.platform == 'win32':
        print(f"   venv\\Scripts\\activate")
    else:
        print(f"   source venv/bin/activate")
    print(f"   uvicorn app.main:app --reload --port 8000\n")
    
    print(f"   {Colors.OKCYAN}Terminal 2 - AI Service:{Colors.ENDC}")
    print(f"   cd ai-service")
    if sys.platform == 'win32':
        print(f"   venv\\Scripts\\activate")
    else:
        print(f"   source venv/bin/activate")
    print(f"   uvicorn app.main:app --reload --port 8001\n")
    
    print(f"   {Colors.OKCYAN}Terminal 3 - Frontend:{Colors.ENDC}")
    print(f"   cd frontend")
    print(f"   python -m http.server 3000\n")
    
    print(f"{Colors.BOLD}4. Access the Application:{Colors.ENDC}")
    print(f"   Frontend: http://localhost:3000")
    print(f"   Backend API Docs: http://localhost:8000/api/docs")
    print(f"   AI Service Docs: http://localhost:8001/api/docs\n")
    
    print(f"{Colors.BOLD}5. Read Documentation:{Colors.ENDC}")
    print(f"   - README.md - Project overview")
    print(f"   - IMPLEMENTATION_PLAN.md - Implementation guide")
    print(f"   - SYSTEM_ARCHITECTURE.md - Technical details\n")

def main():
    """Main setup function"""
    print_header("Oscar Legal Practitioners - Setup")
    print(f"{Colors.WARNING}⚠ ACADEMIC DISCLAIMER: This is for educational purposes only{Colors.ENDC}\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check PostgreSQL
    check_postgresql()
    
    # Create directory structure
    create_directory_structure()
    
    # Create .env file
    create_env_file()
    
    # Set up virtual environments
    print_header("Setting Up Virtual Environments")
    
    response = input("Set up backend virtual environment? (y/n): ")
    if response.lower() == 'y':
        setup_backend_venv()
    
    response = input("Set up AI service virtual environment? (y/n): ")
    if response.lower() == 'y':
        setup_ai_venv()
    
    # Create database
    print_header("Database Setup")
    create_database()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        sys.exit(1)
