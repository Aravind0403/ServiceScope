import os
import ast
import json

def extract_http_calls_from_file(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=file_path)

    calls = []

    class APICallVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            try:
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "requests":
                        if node.func.attr in ["get", "post", "put", "delete"]:
                            url_arg = node.args[0]
                            if isinstance(url_arg, ast.Constant):
                                calls.append({
                                    "method": node.func.attr,
                                    "url": url_arg.value,
                                    "line": node.lineno
                                })
            except Exception as e:
                print(f"Error while parsing {file_path}: {e}")
            self.generic_visit(node)

    visitor = APICallVisitor()
    visitor.visit(tree)

    return calls


def walk_and_extract_calls(base_dir):
    all_calls = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                file_calls = extract_http_calls_from_file(full_path)
                for call in file_calls:
                    rel_path = os.path.relpath(full_path, base_dir)
                    parts = rel_path.split(os.sep)
                    call["file"] = rel_path
                    call["service"] = parts[0] if parts else "unknown"
                    all_calls.append(call)

    return all_calls


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    samples_dir = os.path.join(root_dir, "Samples")
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "api_calls.json")

    print(f"🔍 Scanning directory: {samples_dir}")
    results = walk_and_extract_calls(samples_dir)

    if not results:
        print("🚫 No HTTP calls found.")
    else:
        print(f"\n✅ Found {len(results)} API calls:\n")
        for call in results:
            print(f"📄 [{call['service']}] {call['file']} (line {call['line']}): {call['method'].upper()} {call['url']}")

    # Save results to JSON
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Saved extracted API calls to: {output_file}")