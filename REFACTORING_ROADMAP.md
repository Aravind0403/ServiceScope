# 🗺️ ServiceScope Refactoring Roadmap

**Goal:** Transform from prototype scripts to production-ready AI-native SaaS platform
**Timeline:** 4-6 weeks (aggressive but achievable)
**Approach:** Iterative, with deployable increments

---

## 🏗️ Target Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React/Next.js)                 │
│                   WebSocket + REST API Client                │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application Layer                  │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐ │
│  │  Auth    │  Repos   │  Tasks   │  Graph   │ WebSocket │ │
│  │  Routes  │  Routes  │  Routes  │  Routes  │  Handler  │ │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                    │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐ │
│  │  Repo    │ Extract  │ Infer    │  Graph   │   User    │ │
│  │ Service  │ Service  │ Service  │ Service  │  Service  │ │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Celery Task Queue (Redis)                  │
│  ┌──────────────────┬──────────────────┬─────────────────┐ │
│  │  repo_ingestion  │  ast_extraction  │  llm_inference  │ │
│  │      task        │       task       │      task       │ │
│  └──────────────────┴──────────────────┴─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────────┬──────────────────┬─────────────────┐ │
│  │   PostgreSQL     │      Neo4j       │     Redis       │ │
│  │  (Users, Repos,  │  (Dependency     │   (Cache +      │ │
│  │   Tasks, Tenants)│     Graph)       │   Sessions)     │ │
│  └──────────────────┴──────────────────┴─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📅 Phase 1: Foundation (Week 1) - CRITICAL

### **Goal:** Working FastAPI + PostgreSQL + Celery stack

### Day 1-2: FastAPI Setup
- [ ] Create new project structure
  ```
  servicescope/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py                 # FastAPI app
  │   ├── config.py               # Settings
  │   ├── dependencies.py         # DI
  │   ├── api/
  │   │   ├── __init__.py
  │   │   ├── v1/
  │   │   │   ├── __init__.py
  │   │   │   ├── auth.py
  │   │   │   ├── repositories.py
  │   │   │   ├── tasks.py
  │   │   │   └── graph.py
  │   ├── models/
  │   │   ├── __init__.py
  │   │   ├── user.py
  │   │   ├── repository.py
  │   │   ├── task.py
  │   │   └── dependency.py
  │   ├── schemas/
  │   │   ├── __init__.py
  │   │   ├── user.py
  │   │   ├── repository.py
  │   │   ├── task.py
  │   │   └── dependency.py
  │   ├── services/
  │   │   ├── __init__.py
  │   │   ├── auth_service.py
  │   │   ├── repo_service.py
  │   │   ├── extraction_service.py
  │   │   ├── inference_service.py
  │   │   └── graph_service.py
  │   ├── tasks/
  │   │   ├── __init__.py
  │   │   ├── celery_app.py
  │   │   ├── repo_tasks.py
  │   │   ├── extraction_tasks.py
  │   │   └── inference_tasks.py
  │   └── core/
  │       ├── __init__.py
  │       ├── security.py
  │       ├── database.py
  │       └── neo4j.py
  ├── migrations/
  ├── tests/
  ├── docker/
  ├── requirements/
  │   ├── base.txt
  │   ├── dev.txt
  │   └── prod.txt
  ├── docker-compose.yml
  ├── alembic.ini
  └── pyproject.toml
  ```

- [ ] Install dependencies
  ```
  fastapi[all]
  uvicorn[standard]
  sqlalchemy
  alembic
  psycopg2-binary
  celery[redis]
  redis
  pydantic
  pydantic-settings
  python-jose[cryptography]
  passlib[bcrypt]
  python-multipart
  ```

- [ ] Create FastAPI app with basic endpoints
  ```python
  # Health check
  GET /health

  # API info
  GET /api/v1/info
  ```

### Day 3-4: PostgreSQL Setup
- [ ] Design database schema
  ```sql
  -- Users table (multi-tenant)
  users (
    id UUID PK,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    is_active BOOLEAN,
    tenant_id UUID FK,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
  )

  -- Tenants table
  tenants (
    id UUID PK,
    name VARCHAR,
    slug VARCHAR UNIQUE,
    plan VARCHAR,
    created_at TIMESTAMP
  )

  -- Repositories table
  repositories (
    id UUID PK,
    tenant_id UUID FK,
    user_id UUID FK,
    name VARCHAR,
    url VARCHAR,
    status VARCHAR,  -- pending, processing, completed, failed
    created_at TIMESTAMP,
    updated_at TIMESTAMP
  )

  -- Tasks table
  tasks (
    id UUID PK,
    tenant_id UUID FK,
    repository_id UUID FK,
    task_type VARCHAR,
    status VARCHAR,
    celery_task_id VARCHAR,
    result JSONB,
    error TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
  )

  -- Dependencies table (cache for Neo4j)
  dependencies (
    id UUID PK,
    tenant_id UUID FK,
    repository_id UUID FK,
    caller_service VARCHAR,
    callee_service VARCHAR,
    method VARCHAR,
    url VARCHAR,
    file_path VARCHAR,
    line_number INT,
    created_at TIMESTAMP
  )
  ```

- [ ] Set up SQLAlchemy models
- [ ] Set up Alembic migrations
- [ ] Create database connection pool
- [ ] Add CRUD operations

### Day 5-7: Celery Setup
- [ ] Configure Celery with Redis
  ```python
  # celery_app.py
  from celery import Celery

  celery_app = Celery(
      "servicescope",
      broker="redis://localhost:6379/0",
      backend="redis://localhost:6379/0"
  )

  celery_app.conf.update(
      task_serializer="json",
      accept_content=["json"],
      result_serializer="json",
      timezone="UTC",
      enable_utc=True,
      task_track_started=True,
      task_time_limit=30 * 60,  # 30 minutes
  )
  ```

- [ ] Create async tasks
  ```python
  @celery_app.task(bind=True)
  def ingest_repository(self, repo_id: str):
      """Clone and analyze repository"""
      pass

  @celery_app.task(bind=True)
  def extract_dependencies(self, repo_id: str):
      """Extract HTTP calls from code"""
      pass

  @celery_app.task(bind=True)
  def infer_services(self, repo_id: str):
      """Infer service names using LLM"""
      pass

  @celery_app.task(bind=True)
  def build_graph(self, repo_id: str):
      """Load dependencies into Neo4j"""
      pass
  ```

- [ ] Add task chaining/workflows
  ```python
  from celery import chain

  pipeline = chain(
      ingest_repository.s(repo_id),
      extract_dependencies.s(),
      infer_services.s(),
      build_graph.s()
  )
  ```

- [ ] Add progress tracking
- [ ] Add error handling and retries

**Deliverable Week 1:**
- ✅ FastAPI server running
- ✅ PostgreSQL with migrations
- ✅ Celery processing tasks
- ✅ Basic API endpoints working
- ✅ Docker Compose for local dev

---

## 📅 Phase 2: Core Features (Week 2) - CRITICAL

### **Goal:** Repo ingestion + Async pipelines working

### Day 8-10: Repository Ingestion
- [ ] GitHub API integration
  ```python
  class GitHubService:
      async def clone_repository(self, url: str, path: str):
          """Clone repo using GitPython"""

      async def get_repo_metadata(self, url: str):
          """Fetch repo info from GitHub API"""

      async def list_python_files(self, path: str):
          """Find all .py files"""
  ```

- [ ] GitLab support (optional)
- [ ] Local file system support
- [ ] Repository cleanup (temp storage)

### Day 11-12: Async Extraction Pipeline
- [ ] Convert `extract_http_calls.py` to async service
  ```python
  class ExtractionService:
      async def extract_from_repository(
          self,
          repo_id: str
      ) -> List[HTTPCall]:
          """Extract all HTTP calls asynchronously"""

      async def extract_from_file(
          self,
          file_path: str
      ) -> List[HTTPCall]:
          """Extract calls from single file"""
  ```

- [ ] Support multiple HTTP libraries
  - requests
  - httpx
  - aiohttp
  - urllib

- [ ] Parallel file processing
- [ ] Progress updates via WebSocket

### Day 13-14: Async Inference Pipeline
- [ ] Convert LLM inference to async
  ```python
  class InferenceService:
      async def infer_service_name(
          self,
          caller: str,
          url: str,
          method: str
      ) -> str:
          """Infer service name using LLM"""

      async def batch_infer(
          self,
          calls: List[HTTPCall]
      ) -> List[Dependency]:
          """Process multiple calls in parallel"""
  ```

- [ ] Add LLM provider abstraction
  - Ollama (local)
  - OpenAI (cloud)
  - Anthropic (cloud)

- [ ] Add caching for repeated URLs
- [ ] Rate limiting

**Deliverable Week 2:**
- ✅ GitHub repos can be ingested
- ✅ Async extraction working
- ✅ Async LLM inference working
- ✅ Full pipeline: URL → Graph in < 5 min
- ✅ Task status tracking

---

## 📅 Phase 3: Platform Features (Week 3) - HIGH PRIORITY

### **Goal:** Authentication + Multi-tenancy + Real-time updates

### Day 15-17: Authentication & Authorization
- [ ] JWT token auth
  ```python
  # Auth endpoints
  POST /api/v1/auth/register
  POST /api/v1/auth/login
  POST /api/v1/auth/refresh
  POST /api/v1/auth/logout
  GET  /api/v1/auth/me
  ```

- [ ] OAuth2 password flow
- [ ] Role-based access control (RBAC)
  - Admin
  - User
  - Viewer

- [ ] Tenant isolation middleware
  ```python
  async def get_current_tenant(
      token: str = Depends(oauth2_scheme)
  ) -> Tenant:
      """Extract tenant from JWT"""
  ```

### Day 18-19: Multi-tenancy
- [ ] Tenant onboarding flow
- [ ] Tenant-scoped queries
- [ ] Resource limits per tenant
- [ ] Billing hooks (Stripe ready)

### Day 20-21: Real-time Updates
- [ ] WebSocket endpoints
  ```python
  @app.websocket("/ws/{tenant_id}/tasks/{task_id}")
  async def task_progress(websocket: WebSocket, task_id: str):
      """Stream task progress"""
      while True:
          progress = await get_task_progress(task_id)
          await websocket.send_json(progress)
          await asyncio.sleep(1)
  ```

- [ ] Server-Sent Events (SSE) alternative
- [ ] Redis pub/sub for broadcasting
- [ ] React client for WebSocket

**Deliverable Week 3:**
- ✅ User registration and login
- ✅ Protected API endpoints
- ✅ Multi-tenant data isolation
- ✅ Real-time task progress
- ✅ WebSocket working

---

## 📅 Phase 4: Production Ready (Week 4) - MEDIUM PRIORITY

### **Goal:** Testing + Observability + CI/CD

### Day 22-24: Testing
- [ ] Unit tests (pytest)
  ```python
  tests/
  ├── unit/
  │   ├── test_extraction.py
  │   ├── test_inference.py
  │   ├── test_graph.py
  │   └── test_services.py
  ├── integration/
  │   ├── test_api.py
  │   ├── test_celery.py
  │   └── test_database.py
  └── e2e/
      └── test_pipeline.py
  ```

- [ ] Integration tests
- [ ] E2E tests
- [ ] Coverage > 80%
- [ ] Fixtures and factories

### Day 25-26: Observability
- [ ] Structured logging
  ```python
  import structlog

  logger = structlog.get_logger()
  logger.info("repo_ingested", repo_id=repo.id, tenant_id=tenant.id)
  ```

- [ ] Prometheus metrics
  ```python
  from prometheus_client import Counter, Histogram

  repo_ingestion_count = Counter(
      "repo_ingestion_total",
      "Total repository ingestions"
  )

  extraction_duration = Histogram(
      "extraction_duration_seconds",
      "Time spent extracting dependencies"
  )
  ```

- [ ] OpenTelemetry tracing
- [ ] Health check endpoints
- [ ] Sentry error tracking

### Day 27-28: CI/CD
- [ ] GitHub Actions workflow
  ```yaml
  # .github/workflows/ci.yml
  name: CI/CD

  on: [push, pull_request]

  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - name: Run tests
          run: pytest tests/ --cov
        - name: Upload coverage
          uses: codecov/codecov-action@v2

    build:
      runs-on: ubuntu-latest
      steps:
        - name: Build Docker image
          run: docker build -t servicescope:${{ github.sha }} .
        - name: Push to registry
          run: docker push servicescope:${{ github.sha }}
  ```

- [ ] Automated testing
- [ ] Docker image builds
- [ ] Deployment automation

**Deliverable Week 4:**
- ✅ Test coverage > 80%
- ✅ Metrics and logging
- ✅ CI/CD pipeline
- ✅ Error tracking
- ✅ Production monitoring

---

## 📅 Phase 5: Advanced Features (Week 5-6) - OPTIONAL

### Week 5: Enhanced Features
- [ ] Advanced LLM features
  - Context-aware inference
  - Multi-model ensemble
  - Confidence scores

- [ ] Graph analytics
  - Circular dependency detection
  - Critical path analysis
  - Service health scoring

- [ ] API rate limiting
- [ ] Caching strategies
- [ ] Background cleanup jobs

### Week 6: Polish & Optimization
- [ ] Performance optimization
  - Database query optimization
  - Caching layer
  - Async everywhere

- [ ] Security hardening
  - OWASP top 10
  - Input validation
  - SQL injection prevention
  - XSS prevention

- [ ] API documentation
  - OpenAPI/Swagger
  - Postman collections
  - Code examples

- [ ] Admin dashboard
  - User management
  - Tenant management
  - Task monitoring

**Deliverable Week 5-6:**
- ✅ Production-grade features
- ✅ Security hardened
- ✅ Performance optimized
- ✅ Fully documented

---

## 🎯 Staff-Level Engineering Checklist

### Architecture & Design
- [ ] Clean architecture (layered)
- [ ] SOLID principles applied
- [ ] Design patterns documented
- [ ] Scalability considerations
- [ ] Trade-off analysis documented

### Code Quality
- [ ] Type hints everywhere
- [ ] Docstrings (Google style)
- [ ] Pre-commit hooks (black, isort, mypy, flake8)
- [ ] Code review process
- [ ] Consistent naming conventions

### Testing
- [ ] Unit tests > 80% coverage
- [ ] Integration tests
- [ ] E2E tests
- [ ] Performance tests
- [ ] Load tests (Locust)

### Observability
- [ ] Structured logging
- [ ] Metrics (Prometheus)
- [ ] Distributed tracing
- [ ] Error tracking (Sentry)
- [ ] APM (Application Performance Monitoring)

### Security
- [ ] Authentication & authorization
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] Secrets management (Vault)

### DevOps
- [ ] Containerization (Docker)
- [ ] Orchestration (K8s)
- [ ] CI/CD pipeline
- [ ] Infrastructure as Code (Terraform)
- [ ] Monitoring & alerting
- [ ] Backup & disaster recovery

### Documentation
- [ ] API documentation (OpenAPI)
- [ ] Architecture diagrams (C4 model)
- [ ] Deployment guide
- [ ] Development setup guide
- [ ] Troubleshooting guide

---

## 📊 Success Metrics

### Week 1:
- [ ] FastAPI responding to requests
- [ ] PostgreSQL persisting data
- [ ] Celery processing 1 task successfully

### Week 2:
- [ ] Can ingest 1 GitHub repo end-to-end
- [ ] Pipeline completes in < 5 minutes
- [ ] Dependencies shown in Neo4j

### Week 3:
- [ ] 2+ users can use simultaneously
- [ ] Real-time updates working
- [ ] Authentication working

### Week 4:
- [ ] Test coverage > 80%
- [ ] CI/CD deploying automatically
- [ ] Metrics dashboard showing data

### Week 5-6:
- [ ] Can handle 10+ concurrent repos
- [ ] Response time < 200ms (95th percentile)
- [ ] Zero critical security issues

---

## 🚀 Quick Wins (Do First)

1. **FastAPI Hello World** (2 hours)
   - Get something running immediately
   - Builds confidence

2. **PostgreSQL User Table** (3 hours)
   - Real data persistence
   - Foundation for everything

3. **Single Celery Task** (4 hours)
   - Proves async works
   - Unblocks parallel work

4. **GitHub Clone** (3 hours)
   - Core value proposition
   - Enables testing with real repos

5. **WebSocket Echo** (2 hours)
   - Real-time foundation
   - Impressive to demo

---

## ⚠️ Risks & Mitigations

### Risk: Scope Creep
- **Mitigation:** Stick to MVP for each phase
- **Fallback:** Skip advanced features

### Risk: Integration Issues
- **Mitigation:** Test integrations early
- **Fallback:** Use Docker Compose for local env

### Risk: Performance Problems
- **Mitigation:** Profile early, optimize later
- **Fallback:** Add caching aggressively

### Risk: Time Constraints
- **Mitigation:** Parallel work where possible
- **Fallback:** Reduce scope, focus on critical path

---

## 📝 Next Actions

1. **Review this roadmap** - Understand the scope
2. **Set up development environment** - FastAPI skeleton
3. **Start Week 1, Day 1** - Create project structure
4. **Daily standup** - Review progress, adjust plan
5. **Weekly demo** - Show working increment

---

**Remember:** Better to have a working MVP that matches resume claims than a perfect solution that's incomplete. Ship early, iterate fast!
