import sys
import os
import json

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

# Now safe to import
from extraction.extract_http_calls import walk_and_extract_calls
from Inference.infer_service_dependency import infer_dependency_from_call

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "inferred_dependencies.jsonl")

def infer_all_calls_and_save(directory_to_scan):
    all_calls = walk_and_extract_calls(directory_to_scan)

    if not all_calls:
        print("🚫 No HTTP calls found for inference.")
        return

    with open(OUTPUT_FILE, "w") as out_file:
        for call in all_calls:
            file_path = call["file"]
            caller_service = file_path.split("/")[0]
            inferred = infer_dependency_from_call(
                caller_service=caller_service,
                method=call["method"],
                url=call["url"]
            )
            result = {
                "caller": caller_service,
                "callee": inferred,
                "method": call["method"],
                "url": call["url"],
                "file": call["file"],
                "line": call["line"]
            }
            print(f"📡 {caller_service} → {inferred} via {call['method'].upper()} {call['url']}")
            out_file.write(json.dumps(result) + "\n")

    print(f"\n✅ Inference complete. Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    samples_dir = os.path.join(root_dir, "Samples")

    infer_all_calls_and_save(samples_dir)