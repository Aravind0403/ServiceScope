# 🗄️ Neo4j Integration

This directory contains scripts for loading ServiceScope dependency data into Neo4j and visualizing the dependency graph.

## 📁 Files

- **`load_to_neo4j.py`** - Loads inferred dependencies from JSONL into Neo4j graph database
- **`visualize_graph.py`** - Queries Neo4j and generates visual dependency graphs using matplotlib
- **`cypher_queries.md`** - Collection of useful Cypher queries for exploring the graph

## 🚀 Quick Start

### 1. Start Neo4j

```bash
docker-compose up -d neo4j
```

Wait a few seconds for Neo4j to start, then verify it's running at: http://localhost:7474

**Credentials:**
- Username: `neo4j`
- Password: `Ar@v!nd0495()`

### 2. Load Dependencies into Neo4j

```bash
python neo4j_integration/load_to_neo4j.py
```

This will:
- Clear any existing graph data
- Create Service nodes for each service
- Create CALLS relationships with metadata (method, URL, file, line)
- Display statistics about the loaded graph

### 3. Visualize the Graph

```bash
python neo4j_integration/visualize_graph.py
```

This will:
- Fetch the dependency graph from Neo4j
- Generate a visual graph using matplotlib
- Save the image to `data/dependency_graph.png`
- Print a text summary of the dependencies

### 4. Explore in Neo4j Browser

Open http://localhost:7474/browser/ and run queries from `cypher_queries.md`, such as:

```cypher
MATCH (s:Service)-[r:CALLS]->(t:Service)
RETURN s, r, t
```

## 🔄 Full Pipeline

To run the entire pipeline (extraction → inference → Neo4j → visualization):

```bash
python run_pipeline.py
```

Or skip specific steps:

```bash
python run_pipeline.py --skip-extraction --skip-inference
```

## 📊 Graph Schema

### Nodes

**Service**
- Properties:
  - `name` (string) - Service identifier

### Relationships

**CALLS**
- Properties:
  - `method` (string) - HTTP method (GET, POST, PUT, DELETE)
  - `url` (string) - Target URL
  - `file` (string) - Source file path
  - `line` (integer) - Line number in source file

## 🔍 Example Queries

### View all dependencies
```cypher
MATCH (caller:Service)-[r:CALLS]->(callee:Service)
RETURN caller.name, r.method, r.url, callee.name
```

### Find services with most outgoing calls
```cypher
MATCH (s:Service)-[r:CALLS]->()
RETURN s.name as service, count(r) as outgoing_calls
ORDER BY outgoing_calls DESC
```

### Find circular dependencies
```cypher
MATCH (s:Service)-[r:CALLS*2..5]->(s)
RETURN s, r
```

See `cypher_queries.md` for more examples!

## 🛠️ Troubleshooting

### Neo4j connection failed

Make sure Neo4j is running:
```bash
docker-compose up -d neo4j
docker-compose logs neo4j
```

### No dependencies found

Make sure you've run the inference step first:
```bash
python Inference/batch_infer_dependencies.py
```

This should create `data/inferred_dependencies.jsonl`.

### Visualization fails

Ensure matplotlib is installed:
```bash
pip install matplotlib networkx
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## 📚 Additional Resources

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
