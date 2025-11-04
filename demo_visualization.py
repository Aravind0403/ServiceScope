#!/usr/bin/env python3
"""
Demo visualization using JSONL data directly (no Neo4j required)

This script demonstrates the graph visualization without requiring a running Neo4j instance.
"""

import os
import json
import matplotlib.pyplot as plt
import networkx as nx


def load_jsonl_data(jsonl_path):
    """Load dependencies from JSONL file."""
    dependencies = []
    with open(jsonl_path, "r") as f:
        for line in f:
            dependencies.append(json.loads(line))
    return dependencies


def create_graph_from_jsonl(dependencies):
    """Create a NetworkX directed graph from JSONL data."""
    G = nx.DiGraph()

    for dep in dependencies:
        caller = dep["caller"]
        callee = dep["callee"]
        method = dep["method"]
        url = dep["url"]

        # Add nodes
        G.add_node(caller, node_type="service")
        G.add_node(callee, node_type="service")

        # Add edge with metadata
        G.add_edge(caller, callee, method=method, url=url)

    return G


def print_graph_info(G, dependencies):
    """Print detailed graph information."""
    print("\n" + "=" * 70)
    print("📊 SERVICE DEPENDENCY GRAPH ANALYSIS")
    print("=" * 70)

    print(f"\n📦 Total Services: {G.number_of_nodes()}")
    print(f"🔗 Total Dependencies: {G.number_of_edges()}")

    print("\n🔵 Service Nodes:")
    print("-" * 70)
    for node in G.nodes():
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        print(f"  • {node}")
        print(f"    ├─ Incoming calls: {in_degree}")
        print(f"    └─ Outgoing calls: {out_degree}")

    print("\n🔗 Dependencies (Edges):")
    print("-" * 70)
    for dep in dependencies:
        caller = dep["caller"]
        callee = dep["callee"]
        method = dep["method"].upper()
        url = dep["url"]
        file_path = dep["file"]
        line = dep["line"]
        print(f"  {caller} → {callee}")
        print(f"    ├─ Method: {method}")
        print(f"    ├─ URL: {url}")
        print(f"    └─ Source: {file_path}:{line}")
        print()

    # Analysis
    if G.number_of_nodes() > 0:
        out_degrees = dict(G.out_degree())
        in_degrees = dict(G.in_degree())

        if out_degrees:
            max_caller = max(out_degrees, key=out_degrees.get)
            print(f"🔝 Most dependencies: {max_caller} ({out_degrees[max_caller]} outgoing calls)")

        if in_degrees:
            max_callee = max(in_degrees, key=in_degrees.get)
            print(f"🎯 Most called service: {max_callee} ({in_degrees[max_callee]} incoming calls)")

    print("\n" + "=" * 70)


def visualize_graph(G, output_path, dependencies):
    """Generate and save a visualization of the dependency graph."""
    plt.figure(figsize=(14, 10))
    plt.title("Service Dependency Graph (Demo Mode)", fontsize=16, fontweight='bold', pad=20)

    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)

    # Draw nodes with different colors based on their role
    out_degrees = dict(G.out_degree())
    in_degrees = dict(G.in_degree())

    # Color nodes: blue for services that call others, green for services being called
    node_colors = []
    for node in G.nodes():
        if out_degrees[node] > 0 and in_degrees[node] == 0:
            node_colors.append('lightblue')  # Only makes calls
        elif in_degrees[node] > 0 and out_degrees[node] == 0:
            node_colors.append('lightgreen')  # Only receives calls
        else:
            node_colors.append('lightyellow')  # Both

    nx.draw_networkx_nodes(G, pos,
                          node_color=node_colors,
                          node_size=4000,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=2)

    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          arrows=True,
                          arrowsize=25,
                          arrowstyle='->',
                          width=3,
                          connectionstyle='arc3,rad=0.1')

    # Draw labels
    nx.draw_networkx_labels(G, pos,
                           font_size=12,
                           font_weight='bold',
                           font_color='black')

    # Draw edge labels (HTTP methods)
    edge_labels = {}
    for dep in dependencies:
        edge_labels[(dep["caller"], dep["callee"])] = dep["method"].upper()

    nx.draw_networkx_edge_labels(G, pos,
                                edge_labels,
                                font_size=10,
                                font_color='red',
                                font_weight='bold')

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightblue', edgecolor='black', label='Caller only'),
        Patch(facecolor='lightgreen', edgecolor='black', label='Callee only'),
        Patch(facecolor='lightyellow', edgecolor='black', label='Both')
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

    plt.axis('off')
    plt.tight_layout()

    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✅ Graph visualization saved to: {output_path}")

    return G


def main():
    """Main demo function."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    jsonl_path = os.path.join(current_dir, "data", "inferred_dependencies.jsonl")
    output_path = os.path.join(current_dir, "data", "dependency_graph_demo.png")

    print("🚀 ServiceScope Graph Visualizer (Demo Mode)")
    print("=" * 70)
    print("\nℹ️  Running in demo mode - using JSONL data directly")
    print("   (Neo4j not required for this demo)\n")

    if not os.path.exists(jsonl_path):
        print(f"❌ JSONL file not found: {jsonl_path}")
        print("\nPlease run the inference step first:")
        print("   python Inference/batch_infer_dependencies.py")
        return

    print(f"📁 Loading data from: {jsonl_path}")
    dependencies = load_jsonl_data(jsonl_path)

    if not dependencies:
        print("⚠️  No dependencies found in JSONL file")
        return

    print(f"✅ Loaded {len(dependencies)} dependencies")

    # Create graph
    G = create_graph_from_jsonl(dependencies)

    # Print analysis
    print_graph_info(G, dependencies)

    # Generate visualization
    print("\n📊 Generating visual graph...")
    visualize_graph(G, output_path, dependencies)

    print("\n✨ Demo complete!")
    print(f"\n📊 View the generated graph: {output_path}")
    print("\n💡 To use with Neo4j:")
    print("   1. Start Neo4j: docker-compose up -d neo4j")
    print("   2. Load data: python neo4j_integration/load_to_neo4j.py")
    print("   3. Visualize: python neo4j_integration/visualize_graph.py")
    print("   4. Browse: http://localhost:7474/browser/\n")


if __name__ == "__main__":
    main()
