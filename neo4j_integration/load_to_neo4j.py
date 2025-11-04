"""
Neo4j Loader for ServiceScope Dependency Graph

This script reads inferred_dependencies.jsonl and loads the data into Neo4j,
creating a graph of service dependencies.
"""

import os
import json
from neo4j import GraphDatabase


class Neo4jLoader:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="Ar@v!nd0495()"):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(f"🔌 Connected to Neo4j at {uri}")

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()
        print("🔌 Neo4j connection closed")

    def clear_database(self):
        """Clear all nodes and relationships from the database."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("🗑️  Database cleared")

    def create_service_node(self, tx, service_name):
        """Create a Service node if it doesn't exist."""
        query = """
        MERGE (s:Service {name: $service_name})
        RETURN s
        """
        tx.run(query, service_name=service_name)

    def create_dependency_relationship(self, tx, caller, callee, method, url, file_path, line):
        """Create a CALLS relationship between two services."""
        query = """
        MATCH (caller:Service {name: $caller})
        MATCH (callee:Service {name: $callee})
        MERGE (caller)-[r:CALLS {
            method: $method,
            url: $url,
            file: $file_path,
            line: $line
        }]->(callee)
        RETURN r
        """
        tx.run(query,
               caller=caller,
               callee=callee,
               method=method.upper(),
               url=url,
               file_path=file_path,
               line=line)

    def load_dependencies_from_jsonl(self, jsonl_path):
        """Load dependencies from JSONL file into Neo4j."""
        if not os.path.exists(jsonl_path):
            print(f"❌ File not found: {jsonl_path}")
            return

        with open(jsonl_path, "r") as f:
            dependencies = [json.loads(line) for line in f]

        if not dependencies:
            print("⚠️  No dependencies found in JSONL file")
            return

        print(f"📦 Loading {len(dependencies)} dependencies into Neo4j...")

        with self.driver.session() as session:
            # First pass: Create all service nodes
            services = set()
            for dep in dependencies:
                services.add(dep["caller"])
                if dep["callee"]:  # Only add if callee was successfully inferred
                    services.add(dep["callee"])

            for service in services:
                session.execute_write(self.create_service_node, service)

            print(f"✅ Created {len(services)} service nodes")

            # Second pass: Create relationships
            relationship_count = 0
            for dep in dependencies:
                if dep["callee"]:  # Only create relationship if callee exists
                    session.execute_write(
                        self.create_dependency_relationship,
                        dep["caller"],
                        dep["callee"],
                        dep["method"],
                        dep["url"],
                        dep["file"],
                        dep["line"]
                    )
                    relationship_count += 1
                    print(f"  📡 {dep['caller']} → {dep['callee']} ({dep['method'].upper()} {dep['url']})")

            print(f"\n✅ Created {relationship_count} dependency relationships")

    def get_graph_stats(self):
        """Get statistics about the loaded graph."""
        with self.driver.session() as session:
            # Count services
            service_count = session.run("MATCH (s:Service) RETURN count(s) as count").single()["count"]

            # Count relationships
            relationship_count = session.run("MATCH ()-[r:CALLS]->() RETURN count(r) as count").single()["count"]

            print(f"\n📊 Graph Statistics:")
            print(f"   Services: {service_count}")
            print(f"   Dependencies: {relationship_count}")


def main():
    """Main function to load dependencies into Neo4j."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    jsonl_path = os.path.join(project_root, "data", "inferred_dependencies.jsonl")

    print("🚀 ServiceScope Neo4j Loader\n")

    loader = Neo4jLoader()

    try:
        # Clear existing data
        print("🗑️  Clearing existing graph data...")
        loader.clear_database()

        # Load new data
        print(f"\n📁 Loading from: {jsonl_path}")
        loader.load_dependencies_from_jsonl(jsonl_path)

        # Show statistics
        loader.get_graph_stats()

        print("\n✨ Neo4j loading complete!")
        print(f"🌐 View graph at: http://localhost:7474/browser/")
        print(f"   Username: neo4j")
        print(f"   Password: Ar@v!nd0495()")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        loader.close()


if __name__ == "__main__":
    main()
