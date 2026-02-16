# Oscar Legal Practitioners - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

This guide will get you up and running quickly.

### Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.11 or higher installed
- ✅ PostgreSQL 15+ installed and running
- ✅ Git installed

### Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone <your-repo-url>
cd oscar-legal-practitioners

# Run the automated setup script
python scripts/setup.py
```

The setup script will:
- Create all necessary directories
- Set up virtual environments
- Install all dependencies
- Create .env file from template

### Step 2: Configure Environment (1 minute)

Edit the `.env` file and update:

```env
# Required: Change this to a secure random string
SECRET_KEY=your-very-long-random-secret-key-here

# Required: Add your OpenAI API key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Update database password if needed
DB_PASSWORD=postgres
```

**Generate a secure SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Initialize Database (1 minute)

```bash
# Activate backend environment
cd backend

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Run migrations
alembic upgrade head

# Optional: Seed sample data
python ../scripts/seed_data.py
```

### Step 4: Start Services (1 minute)

Open **three terminal windows**:

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - AI Service:**
```bash
cd ai-service
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload --port 8001
```

**Terminal 3 - Frontend:**
```bash
cd frontend
python -m http.server 3000
```

### Step 5: Access the Application

Open your browser and visit:

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/api/docs
- **AI Service Docs**: http://localhost:8001/api/docs

---

## 🐳 Alternative: Docker Quick Start

If you prefer Docker:

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your API keys

# Start all services
docker-compose up --build
```

Access at:
- **Frontend**: http://localhost
- **Backend**: http://localhost:8000/api/docs
- **AI Service**: http://localhost:8001/api/docs

---

## 🎯 First Steps After Setup

### 1. Create an Admin User

```bash
cd backend
venv\Scripts\activate
python ../scripts/create_admin.py
```

### 2. Test the API

Visit http://localhost:8000/api/docs and try:
- POST `/api/v1/auth/register` - Create a user
- POST `/api/v1/auth/login` - Get access token

### 3. Explore the Frontend

- Visit http://localhost:3000
- Sign up for an account
- Explore the features

---

## 🔧 Troubleshooting

### Python Version Error
```bash
# Check Python version
python --version

# Should be 3.11 or higher
# If not, install Python 3.11+ from python.org
```

### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
# Windows:
services.msc  # Look for PostgreSQL service

# Linux:
sudo systemctl status postgresql

# Mac:
brew services list
```

### Port Already in Use
```bash
# Change ports in .env or docker-compose.yml
# Or kill the process using the port

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Module Not Found Error
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### OpenAI API Error
- Ensure your API key is correct in `.env`
- Check your OpenAI account has credits
- Verify internet connection

---

## 📚 Next Steps

1. **Read the Documentation**
   - [README.md](../README.md) - Project overview
   - [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) - Development guide
   - [SYSTEM_ARCHITECTURE.md](../SYSTEM_ARCHITECTURE.md) - Technical details

2. **Start Development**
   - Follow the implementation plan
   - Start with Phase 1: Foundation
   - Build features incrementally

3. **Join the Community**
   - Check GitHub Issues
   - Contribute improvements
   - Share your learning

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the documentation** in the `docs/` folder
2. **Search existing issues** on GitHub
3. **Create a new issue** with details:
   - Your OS and Python version
   - Error messages
   - Steps to reproduce

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend starts without errors
- [ ] AI service starts without errors
- [ ] Frontend loads in browser
- [ ] Can access API documentation
- [ ] Database connection works
- [ ] Can create a user account
- [ ] Can login and get JWT token

---

**Happy Coding! 🎉**

Remember: This is an educational project. Always consult licensed professionals for actual legal matters.
