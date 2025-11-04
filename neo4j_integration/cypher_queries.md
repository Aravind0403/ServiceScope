# 🔍 Neo4j Cypher Queries for ServiceScope

This file contains useful Cypher queries for exploring and visualizing the service dependency graph.

## 📊 Basic Queries

### View All Services
```cypher
MATCH (s:Service)
RETURN s
```

### View All Dependencies
```cypher
MATCH (caller:Service)-[r:CALLS]->(callee:Service)
RETURN caller, r, callee
```

### View Complete Dependency Graph
```cypher
MATCH (s:Service)-[r:CALLS]->(t:Service)
RETURN s, r, t
```

## 🔎 Analysis Queries

### Count Total Services
```cypher
MATCH (s:Service)
RETURN count(s) as total_services
```

### Count Total Dependencies
```cypher
MATCH ()-[r:CALLS]->()
RETURN count(r) as total_dependencies
```

### Find Services with Most Outgoing Dependencies
```cypher
MATCH (s:Service)-[r:CALLS]->()
RETURN s.name as service, count(r) as outgoing_calls
ORDER BY outgoing_calls DESC
```

### Find Services with Most Incoming Dependencies
```cypher
MATCH ()-[r:CALLS]->(s:Service)
RETURN s.name as service, count(r) as incoming_calls
ORDER BY incoming_calls DESC
```

### Find All Dependencies for a Specific Service
```cypher
MATCH (s:Service {name: "service_a"})-[r:CALLS]->(target:Service)
RETURN s, r, target
```

### Find Who Calls a Specific Service
```cypher
MATCH (caller:Service)-[r:CALLS]->(s:Service {name: "payment_service"})
RETURN caller, r, s
```

## 🌐 Advanced Queries

### Find Circular Dependencies
```cypher
MATCH (s:Service)-[r:CALLS*2..5]->(s)
RETURN s, r
```

### Find Services with No Dependencies (Leaf Services)
```cypher
MATCH (s:Service)
WHERE NOT (s)-[:CALLS]->()
RETURN s.name as leaf_service
```

### Find Services Not Called by Anyone (Entry Points)
```cypher
MATCH (s:Service)
WHERE NOT ()-[:CALLS]->(s)
RETURN s.name as entry_point
```

### Find All HTTP Methods Used
```cypher
MATCH ()-[r:CALLS]->()
RETURN DISTINCT r.method as http_method, count(r) as usage_count
ORDER BY usage_count DESC
```

### Find Dependencies by HTTP Method
```cypher
MATCH (caller:Service)-[r:CALLS {method: "POST"}]->(callee:Service)
RETURN caller, r, callee
```

### Show Dependency Details (with file and line info)
```cypher
MATCH (caller:Service)-[r:CALLS]->(callee:Service)
RETURN
  caller.name as caller,
  callee.name as callee,
  r.method as method,
  r.url as url,
  r.file as file,
  r.line as line
ORDER BY caller.name, callee.name
```

## 🎨 Visualization Queries

### Service Dependency Map (Best for Neo4j Browser Visualization)
```cypher
MATCH path = (s:Service)-[r:CALLS*1..3]->(t:Service)
RETURN path
LIMIT 100
```

### Show Direct Dependencies Only
```cypher
MATCH path = (s:Service)-[r:CALLS]->(t:Service)
RETURN path
```

### Find Longest Dependency Chain
```cypher
MATCH path = (s:Service)-[r:CALLS*]->(t:Service)
RETURN path
ORDER BY length(path) DESC
LIMIT 1
```

## 🧹 Maintenance Queries

### Delete All Data
```cypher
MATCH (n)
DETACH DELETE n
```

### Delete All Relationships Only
```cypher
MATCH ()-[r:CALLS]->()
DELETE r
```

### Update a Service Name
```cypher
MATCH (s:Service {name: "old_name"})
SET s.name = "new_name"
RETURN s
```

## 💡 Tips for Neo4j Browser

1. **Run a query**: Paste any query above into the Neo4j Browser query box and click the play button
2. **Visualize graph**: Results will show as a visual graph by default
3. **Switch to table view**: Click the table icon to see results in tabular format
4. **Export results**: Click the download icon to export data
5. **Style nodes**: Click on a node label in the left panel to customize colors and sizes
6. **Expand relationships**: Double-click a node to expand its connections

## 🎯 Quick Start Workflow

1. Start with viewing all services:
   ```cypher
   MATCH (s:Service) RETURN s
   ```

2. Then view the complete graph:
   ```cypher
   MATCH (s:Service)-[r:CALLS]->(t:Service) RETURN s, r, t
   ```

3. Analyze dependencies:
   ```cypher
   MATCH (s:Service)-[r:CALLS]->()
   RETURN s.name as service, count(r) as outgoing_calls
   ORDER BY outgoing_calls DESC
   ```
