# 🌐 Personal Portfolio Website Plan

**Purpose:** Showcase ServiceScope project and demonstrate staff-level engineering capabilities
**Target:** Technical recruiters, hiring managers, senior engineers
**Timeline:** 1 week (parallel to refactoring)

---

## 🎯 Goals

1. **Demonstrate ServiceScope live** - Working demo with real data
2. **Explain architecture** - Interactive diagrams and technical depth
3. **Show code quality** - GitHub integration, metrics, tests
4. **Prove claims** - Validate resume with evidence
5. **Easy to navigate** - Clean UX for technical audience

---

## 🏗️ Tech Stack

### **Frontend:**
- **Framework:** Next.js 14 (React, TypeScript)
- **Styling:** Tailwind CSS + shadcn/ui
- **Animations:** Framer Motion
- **Charts:** Recharts, D3.js for graph viz
- **Code Display:** Prism.js / highlight.js

### **Backend:**
- **API:** Same FastAPI backend from ServiceScope
- **Demo Mode:** Readonly API for portfolio visitors
- **Live Demo:** Sandboxed environment with rate limiting

### **Hosting:**
- **Frontend:** Vercel (free tier)
- **Backend:** Railway / Render / Fly.io (free tier)
- **Database:** Neon (serverless Postgres)
- **Graph:** Neo4j Aura Free

---

## 📄 Page Structure

### 1. **Landing Page** (`/`)
Hero section with:
- Professional headshot
- Tagline: "Staff Engineer | AI-Native Platforms | Microservices Architecture"
- Quick links: Projects | About | Contact
- Live ServiceScope demo embed

### 2. **ServiceScope Project** (`/projects/servicescope`)

#### **Overview Section:**
```
┌─────────────────────────────────────────────┐
│  ServiceScope - AI Dependency Mapper         │
│  ────────────────────────────────────────    │
│  AI-native platform that automatically       │
│  maps microservice dependencies using        │
│  AST analysis + LLM inference                │
│                                              │
│  [Live Demo] [GitHub] [Architecture]         │
└─────────────────────────────────────────────┘
```

#### **Tech Stack Visual:**
```
Frontend         Backend          Data Layer
────────         ───────          ──────────
React            FastAPI          PostgreSQL
Next.js          Celery           Neo4j
TypeScript       Redis            Redis
Tailwind         SQLAlchemy
```

#### **Key Features:**
- ✅ GitHub repository ingestion
- ✅ AST-based dependency extraction
- ✅ LLM-powered service inference
- ✅ Real-time graph visualization
- ✅ Multi-tenant architecture
- ✅ Async task processing

#### **Live Demo Embed:**
```
┌─────────────────────────────────────────────┐
│  Try It Live                                 │
│  ────────────────────────────────────────    │
│                                              │
│  Repository URL:                             │
│  [https://github.com/username/repo_____]     │
│                                              │
│  [Analyze Repository]                        │
│                                              │
│  ┌─────────────────────────────────────┐    │
│  │ 🔄 Processing...                     │    │
│  │ ✅ Cloned repository                 │    │
│  │ 🔄 Extracting dependencies (45%)     │    │
│  │ ⏳ Inferring services...             │    │
│  │ ⏳ Building graph...                 │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

#### **Interactive Graph:**
Real-time Neo4j visualization using vis.js or D3.js
- Draggable nodes
- Zoom/pan
- Click nodes for details
- Filter by HTTP method
- Highlight circular dependencies

#### **Architecture Deep Dive:**

**System Architecture Diagram:**
```
┌────────────────────────────────────────────────────┐
│                   User Browser                      │
│         React SPA + WebSocket Client                │
└────────────────────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────┐
│                   API Gateway                       │
│         FastAPI (ASGI) + Auth Middleware            │
│  ┌──────────┬──────────┬──────────┬──────────┐    │
│  │  /auth   │  /repos  │  /tasks  │  /graph  │    │
│  └──────────┴──────────┴──────────┴──────────┘    │
└────────────────────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ PostgreSQL  │ │    Redis    │ │   Neo4j     │
│ (Users,     │ │  (Cache,    │ │(Dependency  │
│  Repos,     │ │   Queue,    │ │   Graph)    │
│  Tasks)     │ │   Sessions) │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Celery Workers  │
              │  ┌────┬────┬────┐│
              │  │ W1 │ W2 │ W3 ││
              │  └────┴────┴────┘│
              └─────────────────┘
```

**Data Flow Diagram:**
```
1. User submits GitHub URL
   ↓
2. FastAPI creates task in DB
   ↓
3. Celery picks up task
   ↓
4. Clone repository (async)
   ↓
5. Extract dependencies (parallel)
   ↓
6. Infer services (LLM batch)
   ↓
7. Load to Neo4j (transaction)
   ↓
8. WebSocket notifies user
   ↓
9. Frontend fetches graph
```

#### **Code Walkthrough:**

**Tab 1: Extraction Service**
```python
# Show actual code with syntax highlighting
class ExtractionService:
    async def extract_from_repository(
        self, repo_id: str
    ) -> List[HTTPCall]:
        """
        Extract HTTP calls from repository using AST.

        Staff-level considerations:
        - Parallel file processing
        - Error handling per file
        - Memory-efficient streaming
        - Progress tracking
        """
        # ... code ...
```

**Tab 2: LLM Inference**
```python
class InferenceService:
    async def infer_service_name(
        self, url: str, context: str
    ) -> str:
        """
        Use LLM to infer service name from URL.

        Staff-level considerations:
        - Rate limiting
        - Caching
        - Fallback strategies
        - Cost optimization
        """
        # ... code ...
```

**Tab 3: Celery Pipeline**
```python
@celery_app.task(bind=True, max_retries=3)
def process_repository(self, repo_id: str):
    """
    Main pipeline task with error handling.

    Staff-level considerations:
    - Idempotency
    - Retry logic
    - Circuit breaker pattern
    - Observable side effects
    """
    # ... code ...
```

#### **Technical Decisions:**

**Decision 1: Why Celery over AWS Lambda?**
- Long-running tasks (> 15 min)
- Cost predictability
- Local development ease
- State management

**Decision 2: Why Neo4j over PostgreSQL for graph?**
- Graph queries (Cypher) > SQL for relationships
- Performance on deep traversals
- Built-in graph algorithms
- Visualization tools

**Decision 3: Why Ollama over OpenAI?**
- Cost: $0 vs $0.002/call
- Privacy: local processing
- Latency: no network calls
- Fallback: OpenAI for prod

#### **Performance Metrics:**

```
┌─────────────────────────────────────────────┐
│  Performance Benchmarks                      │
│  ────────────────────────────────────────    │
│                                              │
│  Repository Ingestion:  < 2 min (1k files)  │
│  Dependency Extraction: < 30 sec            │
│  LLM Inference:         < 10 sec (batch)    │
│  Graph Loading:         < 5 sec             │
│  Total Pipeline:        < 3 min             │
│                                              │
│  API Response Time:     p95 < 200ms         │
│  WebSocket Latency:     < 50ms              │
│  Concurrent Users:      100+ (tested)       │
└─────────────────────────────────────────────┘
```

#### **Testing & Quality:**

```
┌─────────────────────────────────────────────┐
│  Code Quality Metrics                        │
│  ────────────────────────────────────────    │
│                                              │
│  Test Coverage:     87%                      │
│  Unit Tests:        245 passed               │
│  Integration:       32 passed                │
│  E2E Tests:         8 passed                 │
│                                              │
│  Type Coverage:     95% (mypy)               │
│  Linting:           0 errors (flake8)        │
│  Security:          A+ (bandit)              │
│  Performance:       No bottlenecks (profiled)│
└─────────────────────────────────────────────┘
```

#### **Deployment:**

```
Production Environment
──────────────────────
Platform:      Railway / Render
Database:      Neon (Serverless Postgres)
Graph:         Neo4j Aura
Cache:         Upstash Redis
Workers:       3x Celery workers
Monitoring:    Sentry + Prometheus
Logging:       Structured JSON logs
CI/CD:         GitHub Actions
Uptime:        99.9% SLA
```

### 3. **Architecture Page** (`/projects/servicescope/architecture`)

Interactive C4 diagrams:
- **Level 1:** System Context
- **Level 2:** Container Diagram
- **Level 3:** Component Diagram
- **Level 4:** Code Examples

### 4. **About Page** (`/about`)

- Professional summary
- Tech stack expertise
- Work experience
- Education
- Certifications

### 5. **Contact Page** (`/contact`)

- Email
- LinkedIn
- GitHub
- Twitter
- Calendar booking link

---

## 🎨 Design Mockup

### **Color Scheme:**
```
Primary:    #2563eb (blue-600)
Secondary:  #7c3aed (violet-600)
Accent:     #06b6d4 (cyan-500)
Background: #0f172a (slate-900)
Text:       #f1f5f9 (slate-100)
Code BG:    #1e293b (slate-800)
```

### **Typography:**
```
Headings:   Inter (Google Fonts)
Body:       Inter
Code:       Fira Code / JetBrains Mono
```

### **Layout:**
```
┌──────────────────────────────────────────────┐
│  [Logo]              About  Projects  Contact│  ← Nav
├──────────────────────────────────────────────┤
│                                              │
│              Hero Section                     │
│          (Full viewport height)              │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│          ServiceScope Showcase               │
│     (Live demo + Architecture + Code)        │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│             Other Projects                   │
│        (Grid of project cards)               │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│            Skills & Experience               │
│         (Timeline + Tech logos)              │
│                                              │
├──────────────────────────────────────────────┤
│              Contact Form                    │
└──────────────────────────────────────────────┘
```

---

## 🚀 Implementation Plan

### **Week 1: Setup + Landing**
- [ ] Day 1: Next.js project setup
- [ ] Day 2: Landing page design
- [ ] Day 3: Navigation + routing
- [ ] Day 4: About page
- [ ] Day 5: Contact page
- [ ] Day 6-7: Deploy to Vercel

### **Week 2: ServiceScope Integration**
- [ ] Day 1-2: Live demo embed
- [ ] Day 3-4: Interactive graph viz
- [ ] Day 5-6: Architecture diagrams
- [ ] Day 7: Code walkthrough sections

### **Week 3: Polish**
- [ ] Day 1-2: Animations (Framer Motion)
- [ ] Day 3-4: SEO optimization
- [ ] Day 5: Performance optimization
- [ ] Day 6-7: Final testing + launch

---

## 📊 Key Features

### **1. Live Demo Sandbox:**
- Visitor can analyze public GitHub repos
- Rate limited (5 repos/day per IP)
- Read-only access
- Progress bar with WebSocket updates
- Results cached for 24h

### **2. Interactive Graph Visualization:**
- D3.js force-directed graph
- Filter by service, method, tenant
- Click nodes for details
- Export as PNG/SVG
- Share graph URL

### **3. Code Snippets:**
- Syntax highlighted
- Copy button
- Language badge
- Line numbers
- Annotations explaining staff-level decisions

### **4. Architecture Diagrams:**
- Interactive C4 models
- Zoom into components
- Hover for descriptions
- Export diagrams

### **5. Metrics Dashboard:**
- Real-time GitHub stats
- Test coverage badge
- Build status
- Performance metrics

---

## 🎯 Content Strategy

### **For Recruiters:**
- Clear project summary
- Tech stack prominently displayed
- "Hire me" CTA
- Resume download link

### **For Engineers:**
- Deep technical dive
- Architecture rationale
- Code walkthroughs
- GitHub link

### **For Managers:**
- Business value explanation
- Success metrics
- Team collaboration stories
- Project timeline

---

## 📱 Responsive Design

### **Mobile:**
- Hamburger menu
- Stacked layout
- Touch-friendly graph
- Simplified diagrams

### **Tablet:**
- Side navigation
- 2-column layout
- Full graph viz

### **Desktop:**
- Fixed sidebar nav
- Multi-column layouts
- Split screen (code + diagram)
- Picture-in-picture demo

---

## 🔧 Technical Implementation

### **Next.js Structure:**
```
portfolio/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                    # Landing
│   ├── about/
│   │   └── page.tsx
│   ├── projects/
│   │   ├── page.tsx                # Projects list
│   │   └── servicescope/
│   │       ├── page.tsx            # Main project page
│   │       ├── architecture/
│   │       │   └── page.tsx
│   │       └── demo/
│   │           └── page.tsx
│   └── contact/
│       └── page.tsx
├── components/
│   ├── ui/                         # shadcn components
│   ├── Hero.tsx
│   ├── ProjectCard.tsx
│   ├── GraphVisualization.tsx
│   ├── ArchitectureDiagram.tsx
│   ├── CodeBlock.tsx
│   ├── LiveDemo.tsx
│   └── Navigation.tsx
├── lib/
│   ├── api.ts                      # API client
│   ├── websocket.ts                # WebSocket client
│   └── utils.ts
├── public/
│   ├── images/
│   ├── diagrams/
│   └── resume.pdf
└── styles/
    └── globals.css
```

### **API Integration:**
```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function analyzeRepository(url: string) {
  const response = await fetch(`${API_BASE}/api/v1/repos/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  return response.json();
}

export function subscribeToTask(taskId: string, callback: Function) {
  const ws = new WebSocket(`${WS_BASE}/ws/tasks/${taskId}`);
  ws.onmessage = (event) => callback(JSON.parse(event.data));
  return ws;
}
```

### **Graph Visualization:**
```typescript
// components/GraphVisualization.tsx
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export function GraphVisualization({ data }) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);

    // Force simulation
    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.edges))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter());

    // Render nodes and edges
    // ... D3 code ...
  }, [data]);

  return <svg ref={svgRef} width="100%" height="600" />;
}
```

---

## 📈 Analytics & Tracking

### **Google Analytics 4:**
- Page views
- Demo usage
- Graph interactions
- Time on page
- Bounce rate

### **Custom Events:**
```javascript
// Track demo usage
gtag('event', 'demo_started', {
  repository_url: url
});

// Track graph interactions
gtag('event', 'graph_node_clicked', {
  service_name: node.name
});
```

---

## 🎓 Staff-Level Considerations

### **1. Performance:**
- Next.js Image optimization
- Code splitting
- Lazy loading
- CDN (Vercel Edge)
- 100 Lighthouse score

### **2. SEO:**
- Server-side rendering
- Meta tags
- Open Graph
- Structured data (JSON-LD)
- Sitemap

### **3. Accessibility:**
- WCAG 2.1 AA compliant
- Keyboard navigation
- Screen reader tested
- Aria labels
- Semantic HTML

### **4. Security:**
- Content Security Policy
- HTTPS only
- Rate limiting
- Input sanitization
- No secrets in frontend

---

## 💰 Hosting Costs

### **Free Tier:**
- **Vercel:** Free (100GB bandwidth)
- **Neon:** Free (3GB storage)
- **Neo4j Aura:** Free (50k nodes)
- **Upstash Redis:** Free (10k commands/day)

**Total:** $0/month 🎉

### **If Scaling Needed:**
- **Vercel Pro:** $20/month
- **Neon Pro:** $19/month
- **Neo4j:** $65/month
- **Upstash:** $10/month

**Total:** $114/month (only if needed)

---

## ✅ Launch Checklist

### **Before Launch:**
- [ ] All pages responsive
- [ ] Live demo working
- [ ] Graph visualization smooth
- [ ] All links functional
- [ ] Resume downloadable
- [ ] Contact form tested
- [ ] Analytics configured
- [ ] SEO optimized
- [ ] Lighthouse score > 90
- [ ] Accessibility tested

### **Launch Day:**
- [ ] Deploy to production
- [ ] Test on multiple devices
- [ ] Share on LinkedIn
- [ ] Share on Twitter
- [ ] Update resume with URL
- [ ] Send to recruiters

### **Post-Launch:**
- [ ] Monitor analytics
- [ ] Fix any bugs
- [ ] Gather feedback
- [ ] Iterate on design
- [ ] Add more projects

---

## 🎯 Success Metrics

**Week 1:**
- [ ] 50+ visitors
- [ ] 10+ demo uses
- [ ] 5+ LinkedIn connections

**Month 1:**
- [ ] 500+ visitors
- [ ] 100+ demo uses
- [ ] 3+ interview requests

**Month 3:**
- [ ] 2000+ visitors
- [ ] 500+ demo uses
- [ ] Job offers

---

**Remember:** The portfolio is a living document. Update it as ServiceScope evolves. Show your journey, not just the destination!
