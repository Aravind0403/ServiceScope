"""
Graph Visualization Utility for ServiceScope

This script queries Neo4j and generates visual representations of the service dependency graph
using matplotlib and networkx.
"""

import os
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import networkx as nx


class GraphVisualizer:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="Ar@v!nd0495()"):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(f"🔌 Connected to Neo4j at {uri}")

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()

    def fetch_graph_data(self):
        """Fetch all services and their dependencies from Neo4j."""
        query = """
        MATCH (caller:Service)-[r:CALLS]->(callee:Service)
        RETURN caller.name as caller,
               callee.name as callee,
               r.method as method,
               r.url as url
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    def create_networkx_graph(self, dependencies):
        """Create a NetworkX directed graph from dependency data."""
        G = nx.DiGraph()

        for dep in dependencies:
            caller = dep["caller"]
            callee = dep["callee"]
            method = dep["method"]
            url = dep["url"]

            # Add nodes
            G.add_node(caller)
            G.add_node(callee)

            # Add edge with metadata
            G.add_edge(caller, callee, method=method, url=url)

        return G

    def visualize_graph(self, output_path="dependency_graph.png", show_labels=True):
        """Generate and save a visualization of the dependency graph."""
        print("📊 Fetching graph data from Neo4j...")
        dependencies = self.fetch_graph_data()

        if not dependencies:
            print("⚠️  No dependencies found to visualize")
            return

        print(f"📦 Found {len(dependencies)} dependencies")

        # Create NetworkX graph
        G = self.create_networkx_graph(dependencies)

        # Set up the plot
        plt.figure(figsize=(14, 10))
        plt.title("Service Dependency Graph", fontsize=16, fontweight='bold')

        # Use hierarchical layout
        try:
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        except:
            pos = nx.circular_layout(G)

        # Draw the graph
        nx.draw_networkx_nodes(G, pos,
                               node_color='lightblue',
                               node_size=3000,
                               alpha=0.9)

        nx.draw_networkx_edges(G, pos,
                               edge_color='gray',
                               arrows=True,
                               arrowsize=20,
                               arrowstyle='->',
                               width=2,
                               connectionstyle='arc3,rad=0.1')

        if show_labels:
            nx.draw_networkx_labels(G, pos,
                                   font_size=10,
                                   font_weight='bold',
                                   font_color='black')

            # Draw edge labels (HTTP methods)
            edge_labels = {}
            for dep in dependencies:
                edge_labels[(dep["caller"], dep["callee"])] = dep["method"]

            nx.draw_networkx_edge_labels(G, pos,
                                        edge_labels,
                                        font_size=8,
                                        font_color='red')

        plt.axis('off')
        plt.tight_layout()

        # Save the figure
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ Graph visualization saved to: {output_path}")

        # Show statistics
        print(f"\n📊 Graph Statistics:")
        print(f"   Nodes (Services): {G.number_of_nodes()}")
        print(f"   Edges (Dependencies): {G.number_of_edges()}")
        print(f"   Avg. out-degree: {sum(dict(G.out_degree()).values()) / G.number_of_nodes():.2f}")

        return G

    def print_graph_summary(self):
        """Print a text summary of the dependency graph."""
        dependencies = self.fetch_graph_data()

        if not dependencies:
            print("⚠️  No dependencies found")
            return

        G = self.create_networkx_graph(dependencies)

        print("\n" + "=" * 60)
        print("📊 SERVICE DEPENDENCY GRAPH SUMMARY")
        print("=" * 60)

        print(f"\n📦 Total Services: {G.number_of_nodes()}")
        print(f"🔗 Total Dependencies: {G.number_of_edges()}")

        print("\n🔵 Services and their outgoing dependencies:")
        print("-" * 60)

        for dep in dependencies:
            caller = dep["caller"]
            callee = dep["callee"]
            method = dep["method"]
            url = dep["url"]
            print(f"  {caller} → {callee}")
            print(f"    └─ {method} {url}")

        # Find services with most dependencies
        out_degrees = dict(G.out_degree())
        if out_degrees:
            max_caller = max(out_degrees, key=out_degrees.get)
            print(f"\n🔝 Most dependencies: {max_caller} ({out_degrees[max_caller]} outgoing calls)")

        # Find most called services
        in_degrees = dict(G.in_degree())
        if in_degrees:
            max_callee = max(in_degrees, key=in_degrees.get)
            print(f"🎯 Most called service: {max_callee} ({in_degrees[max_callee]} incoming calls)")

        print("\n" + "=" * 60)


def main():
    """Main function to visualize the dependency graph."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "..", "data", "dependency_graph.png")

    print("🚀 ServiceScope Graph Visualizer\n")

    visualizer = GraphVisualizer()

    try:
        # Print text summary
        visualizer.print_graph_summary()

        # Generate visual graph
        print("\n📊 Generating visual graph...")
        visualizer.visualize_graph(output_path)

        print("\n✨ Visualization complete!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        visualizer.close()


if __name__ == "__main__":
    main()
