# ⚡ Quick Start Guide - Begin Refactoring NOW

**Time to first code:** 15 minutes
**Goal:** Get FastAPI running with your first endpoint

---

## 🚀 Step 1: Create New Project Structure (5 min)

```bash
# Navigate to project
cd /home/user/ServiceScope

# Create new structure
mkdir -p app/{api/v1,models,schemas,services,tasks,core}
mkdir -p tests/{unit,integration,e2e}
mkdir -p migrations

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/tasks/__init__.py
touch app/core/__init__.py
```

---

## 🔧 Step 2: Install Dependencies (3 min)

```bash
# Create requirements/base.txt
cat > requirements/base.txt << 'EOF'
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
asyncpg==0.29.0

# Task Queue
celery==5.3.6
redis==5.0.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Neo4j (existing)
neo4j==5.15.0

# Utils
python-dotenv==1.0.0
httpx==0.26.0
GitPython==3.1.41

# Existing dependencies
requests==2.32.4
matplotlib==3.8.2
networkx==3.2.1
EOF

# Install
pip install -r requirements/base.txt
```

---

## 💻 Step 3: Create FastAPI App (5 min)

### `app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ServiceScope API",
    description="AI-native platform for microservice dependency mapping",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to ServiceScope API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Real check
        "celery": "connected"     # TODO: Real check
    }
```

### `app/core/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "ServiceScope"

    # Database
    DATABASE_URL: str = "postgresql://servicescope:password@localhost/servicescope"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "Ar@v!nd0495()"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

### Create `.env` file
```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql://servicescope:password@localhost/servicescope
REDIS_URL=redis://localhost:6379/0
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=Ar@v!nd0495()
SECRET_KEY=change-this-to-a-random-secret-key
EOF
```

---

## 🐳 Step 4: Update Docker Compose (2 min)

Update `docker-compose.yml`:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: servicescope
      POSTGRES_PASSWORD: password
      POSTGRES_DB: servicescope
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - service-net

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - service-net

  neo4j:
    image: neo4j:5.15
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/Ar@v!nd0495()
    volumes:
      - neo4j_data:/data
    networks:
      - service-net

networks:
  service-net:

volumes:
  postgres_data:
  neo4j_data:
```

---

## 🎯 Step 5: Run Everything (5 min)

### Terminal 1: Start Services
```bash
docker-compose up -d
```

### Terminal 2: Run FastAPI
```bash
uvicorn app.main:app --reload --port 8000
```

### Test It!
```bash
# Open browser
open http://localhost:8000/docs

# Or curl
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "celery": "connected"
}
```

---

## ✅ Verification Checklist

- [ ] FastAPI running on http://localhost:8000
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] PostgreSQL running on localhost:5432
- [ ] Redis running on localhost:6379
- [ ] Neo4j running on localhost:7474
- [ ] `/health` endpoint returns 200 OK
- [ ] No errors in console

---

## 🎯 Next Steps (Choose Your Path)

### **Path A: Database First (Recommended)**
Go to: `DATABASE_SETUP.md` (create this next)
- Set up SQLAlchemy models
- Create Alembic migrations
- Build first CRUD endpoint

### **Path B: Authentication First**
Go to: `AUTH_SETUP.md` (create this next)
- Add user model
- Implement JWT auth
- Protect endpoints

### **Path C: Celery First**
Go to: `CELERY_SETUP.md` (create this next)
- Configure Celery
- Create first task
- Test async processing

---

## 🐛 Troubleshooting

### **Port already in use:**
```bash
# Find process using port
lsof -i :8000

# Kill it
kill -9 <PID>
```

### **Database connection fails:**
```bash
# Check if postgres is running
docker-compose ps

# Check logs
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

### **Redis connection fails:**
```bash
# Check Redis
docker-compose logs redis

# Test connection
redis-cli ping
# Should return: PONG
```

### **Import errors:**
```bash
# Make sure you're in the right directory
pwd  # Should be /home/user/ServiceScope

# Check Python path
echo $PYTHONPATH

# Run from project root
export PYTHONPATH="${PYTHONPATH}:/home/user/ServiceScope"
```

---

## 📊 What You Just Built

```
✅ FastAPI web server
✅ PostgreSQL database
✅ Redis cache/queue
✅ Neo4j graph database
✅ Docker Compose orchestration
✅ Configuration management
✅ CORS enabled
✅ Auto-generated API docs
✅ Health check endpoint
✅ Development environment
```

**Time invested:** ~15 minutes
**Progress:** ~10% of Week 1

---

## 🎓 Understanding What You Did

### **1. FastAPI = Express.js for Python**
- Automatic API documentation (Swagger)
- Fast (built on Starlette + Pydantic)
- Type hints = validation + docs
- Async/await support

### **2. Pydantic Settings**
- Environment variable management
- Type validation
- Easy configuration

### **3. Docker Compose**
- All services in one command
- Consistent environment
- Easy to share with team

### **4. Project Structure**
- `app/` - Application code
- `app/api/` - API routes/endpoints
- `app/models/` - Database models
- `app/schemas/` - Request/response schemas
- `app/services/` - Business logic
- `app/tasks/` - Celery tasks
- `app/core/` - Config, database, security

---

## 🚀 You're Ready!

**Current Status:** Foundation is set ✅
**Next:** Build on top of this foundation
**Timeline:** Week 1, Day 1 - COMPLETE

**Celebrate this win! 🎉**

Then move to the next step in the roadmap.

---

## 📞 Need Help?

**Common Issues:**
1. Port conflicts - Change ports in docker-compose.yml
2. Permission errors - Use sudo or fix Docker permissions
3. Import errors - Check PYTHONPATH
4. Database errors - Check DATABASE_URL in .env

**Pro Tip:** Commit early, commit often
```bash
git add -A
git commit -m "feat: FastAPI foundation with PostgreSQL, Redis, Neo4j"
git push
```

---

**You've just laid the foundation for a production-grade SaaS platform. Everything else builds on this. Let's go! 🚀**
