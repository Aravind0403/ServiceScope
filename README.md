# 🔍 ServiceScope — LLM-Powered Dependency Mapper

This tool extracts HTTP API calls from Python microservices and uses a local LLM (via Ollama) to infer likely target service dependencies. The results are saved as structured data for graph-based analysis.

## 🔧 Features

- 🧠 LLM integration using [Ollama](https://ollama.com/)
- 🕵️ AST-based static analysis of outbound API calls
- 📦 JSONL output for building dependency graphs
- 🔁 Batch mode for processing entire service directories

## 📂 Project Structure

- `Samples/` – Example Python services
- `extraction/` – Static analysis logic
- `inference/` – LLM integration logic
- `data/` – Output files (e.g., `inferred_dependencies.jsonl`)

## 🚀 Running the Inference
python inference/batch_infer_dependencies.py
```bash
  ollama run gemma:3n
```
💡 TODO
	•	Neo4j integration for visual graphs
	•	CI/CD automation for extraction
	•	CLI interface
