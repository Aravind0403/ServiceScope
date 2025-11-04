# 🚀 Local Setup & Execution Guide

This guide shows you how to run ServiceScope locally on your machine with full Neo4j integration.

## ✅ What We Just Demonstrated

### 1. HTTP Call Extraction ✅
**Command:** `python extraction/extract_http_calls.py`

**Result:**
```
🔍 Scanning directory: /home/user/ServiceScope/Samples

✅ Found 2 API calls:

📄 [service_a] service_a/app.py (line 4): GET http://customer-service.internal/api/v1/customers
📄 [service_a] service_a/app.py (line 8): POST http://localhost:5001/api/pay

💾 Saved extracted API calls to: extraction/output/api_calls.json
```

### 2. Graph Visualization ✅
**Command:** `python demo_visualization.py`

**Generated:** `data/dependency_graph_demo.png` (254KB)

**Graph Analysis:**
- **3 Services:** service_a, customer_service, payment_gateway
- **2 Dependencies:**
  - service_a → customer_service (GET)
  - service_a → payment_gateway (POST)

**Visualization Features:**
- Color-coded nodes (blue=caller, green=callee, yellow=both)
- HTTP methods shown on edges (GET/POST)
- Directional arrows showing call flow
- Legend for easy interpretation

---

## 🏠 Running on Your Local Machine

### Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Docker & Docker Compose**
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Ollama** (optional, for LLM inference)
   ```bash
   ollama --version
   ```

### Step-by-Step Setup

#### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `neo4j` - Neo4j Python driver
- `matplotlib` - Graph visualization
- `networkx` - Graph analysis
- `requests` - HTTP client for extraction
- `Flask` - Mock services

#### 2. Start Neo4j

```bash
docker-compose up -d neo4j
```

**Wait 10-15 seconds** for Neo4j to initialize, then verify:

```bash
docker-compose logs neo4j
```

You should see: `Started.`

#### 3. Access Neo4j Browser

Open in your browser: **http://localhost:7474**

**Login credentials:**
- Username: `neo4j`
- Password: `Ar@v!nd0495()`

#### 4. Run Complete Pipeline

**Option A: Full Pipeline (Recommended)**
```bash
python run_pipeline.py
```

This runs all steps:
1. Extract HTTP calls from code
2. Infer service names using LLM (requires Ollama)
3. Load data into Neo4j
4. Generate visualization

**Option B: Individual Steps**

```bash
# Step 1: Extract HTTP calls
python extraction/extract_http_calls.py

# Step 2: Infer dependencies (requires Ollama)
python Inference/batch_infer_dependencies.py

# Step 3: Load into Neo4j
python neo4j_integration/load_to_neo4j.py

# Step 4: Visualize
python neo4j_integration/visualize_graph.py
```

**Option C: Skip LLM (Use Sample Data)**

If you don't have Ollama running:

```bash
# Skip extraction and inference, use existing data
python run_pipeline.py --skip-extraction --skip-inference

# Or just load and visualize
python neo4j_integration/load_to_neo4j.py
python neo4j_integration/visualize_graph.py
```

---

## 🎯 What You'll See

### 1. Neo4j Loader Output

```
🚀 ServiceScope Neo4j Loader

🗑️  Clearing existing graph data...
🗑️  Database cleared

📁 Loading from: /path/to/data/inferred_dependencies.jsonl
📦 Loading 2 dependencies into Neo4j...
✅ Created 3 service nodes

  📡 service_a → customer_service (GET http://customer-service.internal/api/v1/customers)
  📡 service_a → payment_gateway (POST http://localhost:5001/api/pay)

✅ Created 2 dependency relationships

📊 Graph Statistics:
   Services: 3
   Dependencies: 2

✨ Neo4j loading complete!
🌐 View graph at: http://localhost:7474/browser/
```

### 2. Neo4j Browser Visualization

In Neo4j Browser, run this query:

```cypher
MATCH (s:Service)-[r:CALLS]->(t:Service)
RETURN s, r, t
```

**You'll see:**
- Interactive graph with draggable nodes
- Service nodes with labels
- CALLS relationships with arrows
- Click on relationships to see metadata (method, URL, file, line)

### 3. Generated Visualization File

File: `data/dependency_graph.png` (high-quality PNG)

Features:
- Professional graph layout
- Color-coded services
- HTTP methods labeled on edges
- High-resolution (300 DPI)

---

## 🔍 Exploring the Graph

### In Neo4j Browser

**1. View All Services**
```cypher
MATCH (s:Service)
RETURN s
```

**2. Find Services with Most Dependencies**
```cypher
MATCH (s:Service)-[r:CALLS]->()
RETURN s.name as service, count(r) as calls
ORDER BY calls DESC
```

**3. Find All Paths Between Services**
```cypher
MATCH path = (s:Service)-[r:CALLS*1..3]->(t:Service)
RETURN path
```

**4. Get Detailed Dependency Info**
```cypher
MATCH (caller:Service)-[r:CALLS]->(callee:Service)
RETURN caller.name, r.method, r.url, r.file, r.line, callee.name
```

See `neo4j_integration/cypher_queries.md` for 20+ more queries!

---

## 🧪 Testing with Sample Services

The project includes sample services:

### service_a (Samples/service_a/app.py)
```python
import requests

def get_customer_data():
    response = requests.get("http://customer-service.internal/api/v1/customers")
    return response.json()

def process_payment():
    response = requests.post("http://localhost:5001/api/pay")
    return response.status_code
```

### service_b (Samples/service_b/main.py)
```python
import httpx

def generate_report():
    resp = httpx.get("http://reporting-service/api/metrics")
    return resp.json()
```

**Note:** Currently only `requests` library is supported. `httpx` support is on the roadmap.

---

## 🐛 Troubleshooting

### Neo4j connection fails

```bash
# Check if Neo4j container is running
docker-compose ps

# Check logs
docker-compose logs neo4j

# Restart Neo4j
docker-compose restart neo4j

# If still failing, try:
docker-compose down
docker-compose up -d neo4j
```

### Port 7474 already in use

```bash
# Find what's using the port
lsof -i :7474

# Or change port in docker-compose.yml:
ports:
  - "7475:7474"  # Use 7475 instead
```

### Visualization shows no data

```bash
# Check if data exists
cat data/inferred_dependencies.jsonl

# Re-run inference
python Inference/batch_infer_dependencies.py

# Reload Neo4j
python neo4j_integration/load_to_neo4j.py
```

### Ollama not found

```bash
# Install Ollama from https://ollama.com
# Then pull the model:
ollama pull gemma3n:latest

# Or skip LLM inference and use sample data
python run_pipeline.py --skip-inference
```

---

## 📊 Expected Output Structure

```
ServiceScope/
├── data/
│   ├── inferred_dependencies.jsonl    # 320 bytes (2 dependencies)
│   └── dependency_graph.png           # ~254KB (visualization)
├── extraction/
│   └── output/
│       └── api_calls.json             # Extracted HTTP calls
└── neo4j_integration/
    └── (visualization scripts)
```

---

## 🎓 Next Steps

1. **Add More Services**
   - Add your own Python services to `Samples/`
   - They must use the `requests` library
   - Run extraction again

2. **Explore Neo4j Queries**
   - Try queries from `neo4j_integration/cypher_queries.md`
   - Build custom queries for your use case

3. **Customize Visualization**
   - Edit `visualize_graph.py` to change colors, layout, or styling
   - Try different NetworkX layout algorithms

4. **Integrate with CI/CD**
   - Run extraction on every commit
   - Track dependency changes over time
   - Detect breaking changes

---

## 💡 Advanced Usage

### Custom Neo4j Credentials

Edit `docker-compose.yml`:
```yaml
environment:
  - NEO4J_AUTH=neo4j/MySecurePassword123
```

Then update in Python scripts:
```python
Neo4jLoader(uri="bolt://localhost:7687",
            user="neo4j",
            password="MySecurePassword123")
```

### Different LLM Models

Edit `Inference/infer_service_dependency.py`:
```python
def infer_dependency_from_call(caller_service, method, url, model="llama2:latest"):
    # Use different Ollama model
```

### Export Graph Data

```bash
# Export as CSV
cypher-shell -u neo4j -p 'Ar@v!nd0495()' \
  "MATCH (s:Service)-[r:CALLS]->(t:Service)
   RETURN s.name, r.method, r.url, t.name" \
  --format plain > dependencies.csv
```

---

## 📚 Resources

- **Neo4j Browser Guide:** http://localhost:7474/browser/
- **Cypher Query Examples:** `neo4j_integration/cypher_queries.md`
- **Neo4j Documentation:** https://neo4j.com/docs/
- **NetworkX Documentation:** https://networkx.org/
- **Ollama Models:** https://ollama.com/library

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Neo4j Browser accessible at http://localhost:7474
- [ ] Can login with neo4j / Ar@v!nd0495()
- [ ] `extraction/extract_http_calls.py` runs successfully
- [ ] `neo4j_integration/load_to_neo4j.py` loads data without errors
- [ ] Can see services in Neo4j Browser with query: `MATCH (s:Service) RETURN s`
- [ ] `neo4j_integration/visualize_graph.py` generates PNG file
- [ ] Graph visualization shows correct dependencies

---

**Happy Dependency Mapping! 🎉**

For issues or questions, check the main README.md or create an issue on GitHub.
