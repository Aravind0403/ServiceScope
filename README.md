# 🔍 ServiceScope — LLM-Powered Dependency Mapper

This tool extracts HTTP API calls from Python microservices and uses a local LLM (via Ollama) to infer likely target service dependencies. The results are loaded into Neo4j for interactive graph-based analysis and visualization.

## 🔧 Features

- 🧠 **LLM Integration** - Uses [Ollama](https://ollama.com/) for intelligent service name inference
- 🕵️ **AST-based Analysis** - Static analysis of outbound API calls using Python's AST
- 🗄️ **Neo4j Integration** - Graph database for storing and querying service dependencies
- 📊 **Visualization** - Automated dependency graph generation with matplotlib
- 📦 **JSONL Output** - Structured data format for easy processing
- 🔁 **Batch Processing** - Process entire service directories at once

## 📂 Project Structure

```
ServiceScope/
├── Samples/              # Example Python services
│   ├── service_a/       # Makes calls to customer service & payment gateway
│   └── service_b/       # Makes calls to reporting service
├── extraction/          # Static analysis logic
│   ├── extract_http_calls.py
│   └── output/api_calls.json
├── Inference/           # LLM integration logic
│   ├── infer_service_dependency.py
│   └── batch_infer_dependencies.py
├── neo4j_integration/   # Neo4j loader and visualization
│   ├── load_to_neo4j.py
│   ├── visualize_graph.py
│   ├── cypher_queries.md
│   └── README.md
├── data/                # Output files
│   ├── inferred_dependencies.jsonl
│   └── dependency_graph.png
├── docker-compose.yml   # Neo4j and mock services
└── run_pipeline.py      # Complete workflow orchestration
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** with pip
2. **Docker & Docker Compose** for Neo4j
3. **Ollama** for LLM inference (optional if you have pre-inferred data)

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Neo4j
docker-compose up -d neo4j

# Verify Neo4j is running (wait 10-15 seconds for startup)
docker-compose logs neo4j
```

### Run Complete Pipeline

```bash
# Run all steps: extraction → inference → Neo4j → visualization
python run_pipeline.py
```

Or run individual steps:

```bash
# Step 1: Extract HTTP calls from code
python extraction/extract_http_calls.py

# Step 2: Infer service names using LLM (requires Ollama)
python Inference/batch_infer_dependencies.py

# Step 3: Load into Neo4j
python neo4j_integration/load_to_neo4j.py

# Step 4: Generate visualization
python neo4j_integration/visualize_graph.py
```

## 🗄️ Neo4j Integration

### Access Neo4j Browser

Once Neo4j is running, access the browser interface:

- **URL**: http://localhost:7474/browser/
- **Username**: `neo4j`
- **Password**: `Ar@v!nd0495()`

### Load Dependencies

```bash
python neo4j_integration/load_to_neo4j.py
```

This creates:
- **Service nodes** for each microservice
- **CALLS relationships** with metadata (HTTP method, URL, file location)

### Explore with Cypher Queries

View the complete dependency graph:
```cypher
MATCH (s:Service)-[r:CALLS]->(t:Service)
RETURN s, r, t
```

Find services with most dependencies:
```cypher
MATCH (s:Service)-[r:CALLS]->()
RETURN s.name as service, count(r) as outgoing_calls
ORDER BY outgoing_calls DESC
```

See [neo4j_integration/cypher_queries.md](neo4j_integration/cypher_queries.md) for more queries!

### Generate Visualizations

```bash
python neo4j_integration/visualize_graph.py
```

This creates `data/dependency_graph.png` with a visual representation of your service dependencies.

## 🧪 Sample Services

The project includes sample services for testing:

- **service_a** (`Samples/service_a/app.py`)
  - Calls Customer Service API
  - Calls Payment Gateway API

- **service_b** (`Samples/service_b/main.py`)
  - Calls Reporting Service API

## 🔍 How It Works

1. **Extraction** - AST visitor pattern analyzes Python code to find `requests.get/post/put/delete()` calls
2. **Inference** - Ollama LLM (gemma3n) analyzes URLs to infer target service names
3. **Storage** - Dependencies stored as JSONL for easy processing
4. **Graph Loading** - Neo4j driver creates nodes and relationships
5. **Visualization** - NetworkX and matplotlib generate dependency diagrams

## 🛠️ Configuration

### Neo4j Credentials

Update in `docker-compose.yml`:
```yaml
environment:
  - NEO4J_AUTH=neo4j/YourPassword
```

And update in scripts:
- `neo4j_integration/load_to_neo4j.py`
- `neo4j_integration/visualize_graph.py`

### LLM Model

Change the Ollama model in `Inference/infer_service_dependency.py`:
```python
def infer_dependency_from_call(caller_service, method, url, model="gemma3n:latest"):
```

## 📊 Example Output

### JSONL Format
```json
{"caller": "service_a", "callee": "customer_service", "method": "get", "url": "http://customer-service.internal/api/v1/customers", "file": "service_a/app.py", "line": 4}
{"caller": "service_a", "callee": "payment_gateway", "method": "post", "url": "http://localhost:5001/api/pay", "file": "service_a/app.py", "line": 8}
```

### Neo4j Graph Schema

**Nodes:**
- `Service` with property `name`

**Relationships:**
- `CALLS` with properties: `method`, `url`, `file`, `line`

## 🐛 Troubleshooting

### Neo4j connection fails
```bash
# Check if Neo4j is running
docker-compose ps

# View logs
docker-compose logs neo4j

# Restart Neo4j
docker-compose restart neo4j
```

### Ollama not accessible
```bash
# Start Ollama
ollama serve

# Pull the model
ollama pull gemma3n:latest
```

### No dependencies found
Ensure your Python services use the `requests` library. Currently, `httpx` and other HTTP clients are not supported.

## 💡 Roadmap

- ✅ Neo4j integration for visual graphs
- ⬜ Support for more HTTP clients (httpx, aiohttp, urllib)
- ⬜ CI/CD automation for extraction
- ⬜ Interactive CLI interface
- ⬜ Real-time dependency monitoring
- ⬜ API versioning detection
- ⬜ Circular dependency detection and warnings

## 📚 Additional Resources

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Ollama Documentation](https://ollama.com/docs)
- [Python AST Module](https://docs.python.org/3/library/ast.html)

## 📝 License

MIT License - feel free to use and modify as needed!
