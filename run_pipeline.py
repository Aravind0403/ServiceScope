#!/usr/bin/env python3
"""
ServiceScope Pipeline Runner

Orchestrates the complete workflow:
1. Extract HTTP calls from sample services
2. Infer service dependencies using LLM
3. Load dependencies into Neo4j
4. Generate visualization

Usage:
    python run_pipeline.py [--skip-extraction] [--skip-inference] [--skip-neo4j] [--skip-viz]
"""

import os
import sys
import argparse
import subprocess


def run_step(name, script_path, description):
    """Run a pipeline step and handle errors."""
    print("\n" + "=" * 70)
    print(f"🚀 {name}")
    print("=" * 70)
    print(f"📝 {description}")
    print(f"📄 Running: {script_path}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {name} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ {name} failed: {e}")
        return False


def check_neo4j_connection():
    """Check if Neo4j is running and accessible."""
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "Ar@v!nd0495()")
        )
        driver.verify_connectivity()
        driver.close()
        print("✅ Neo4j connection verified")
        return True
    except Exception as e:
        print(f"⚠️  Neo4j connection failed: {e}")
        print("   Make sure Neo4j is running: docker-compose up -d neo4j")
        return False


def check_ollama_connection():
    """Check if Ollama is running and accessible."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama connection verified")
            return True
        else:
            print("⚠️  Ollama API returned non-200 status")
            return False
    except Exception as e:
        print(f"⚠️  Ollama connection failed: {e}")
        print("   Make sure Ollama is running: ollama serve")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run ServiceScope dependency mapping pipeline")
    parser.add_argument("--skip-extraction", action="store_true", help="Skip HTTP call extraction")
    parser.add_argument("--skip-inference", action="store_true", help="Skip LLM inference")
    parser.add_argument("--skip-neo4j", action="store_true", help="Skip Neo4j loading")
    parser.add_argument("--skip-viz", action="store_true", help="Skip visualization")
    parser.add_argument("--check-only", action="store_true", help="Only check dependencies, don't run pipeline")

    args = parser.parse_args()

    # Get project paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    extraction_script = os.path.join(current_dir, "extraction", "extract_http_calls.py")
    inference_script = os.path.join(current_dir, "Inference", "batch_infer_dependencies.py")
    neo4j_loader_script = os.path.join(current_dir, "neo4j_integration", "load_to_neo4j.py")
    visualization_script = os.path.join(current_dir, "neo4j_integration", "visualize_graph.py")

    print("🔍 ServiceScope - Dependency Mapping Pipeline")
    print("=" * 70)

    # Check dependencies
    print("\n🔧 Checking dependencies...")
    neo4j_ok = check_neo4j_connection() if not args.skip_neo4j else True
    ollama_ok = check_ollama_connection() if not args.skip_inference else True

    if args.check_only:
        print("\n✨ Dependency check complete")
        return

    if not args.skip_inference and not ollama_ok:
        print("\n⚠️  Warning: Ollama is not accessible. Inference may fail.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return

    if not args.skip_neo4j and not neo4j_ok:
        print("\n⚠️  Warning: Neo4j is not accessible. Loading may fail.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return

    # Run pipeline steps
    success = True

    # Step 1: Extract HTTP calls
    if not args.skip_extraction:
        success = run_step(
            "Step 1: HTTP Call Extraction",
            extraction_script,
            "Analyzing Python files to extract HTTP API calls using AST"
        )
        if not success:
            print("\n❌ Pipeline failed at extraction step")
            return

    # Step 2: Infer dependencies
    if not args.skip_inference and success:
        success = run_step(
            "Step 2: LLM-based Dependency Inference",
            inference_script,
            "Using Ollama LLM to infer target service names from URLs"
        )
        if not success:
            print("\n❌ Pipeline failed at inference step")
            return

    # Step 3: Load to Neo4j
    if not args.skip_neo4j and success:
        success = run_step(
            "Step 3: Neo4j Graph Loading",
            neo4j_loader_script,
            "Loading inferred dependencies into Neo4j graph database"
        )
        if not success:
            print("\n❌ Pipeline failed at Neo4j loading step")
            return

    # Step 4: Generate visualization
    if not args.skip_viz and success:
        success = run_step(
            "Step 4: Graph Visualization",
            visualization_script,
            "Generating visual representation of the dependency graph"
        )

    # Final summary
    print("\n" + "=" * 70)
    if success:
        print("✨ PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n📊 Output Files:")
        print(f"   • Extracted calls: {current_dir}/extraction/output/api_calls.json")
        print(f"   • Inferred deps:   {current_dir}/data/inferred_dependencies.jsonl")
        print(f"   • Visualization:   {current_dir}/data/dependency_graph.png")
        print("\n🌐 Neo4j Browser:")
        print("   • URL: http://localhost:7474/browser/")
        print("   • User: neo4j")
        print("   • Pass: Ar@v!nd0495()")
        print("\n💡 Next Steps:")
        print("   • Open Neo4j Browser to explore the graph interactively")
        print("   • Run Cypher queries from: neo4j_integration/cypher_queries.md")
        print("   • View the generated visualization: data/dependency_graph.png")
    else:
        print("❌ PIPELINE FAILED")
        print("=" * 70)
        print("\n🔍 Check the error messages above for details")

    print("\n")


if __name__ == "__main__":
    main()
