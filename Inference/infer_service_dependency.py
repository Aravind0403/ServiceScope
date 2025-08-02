import requests

def infer_dependency_from_call(caller_service, method, url, model="gemma3n:latest"):
    prompt = f"""
Given the URL {url} used by {caller_service}, what is the most likely internal service name being called?
Please only return the most probable service name as a short answer like: "payment_service" or "order_service".
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt.strip(),
                "stream": False
            },
            timeout=20
        )

        data = response.json()

        # Safeguard against unexpected structure
        if "response" in data:
            raw_response = data["response"].strip()

            # Basic cleaning: remove quotes, Markdown, or unnecessary punctuation
            cleaned = raw_response.replace("**", "").strip().strip('"').splitlines()[0]

            print(f"📡 Inferred dependency: {cleaned}")
            return cleaned
        else:
            print("⚠️ No response content from LLM.")
            return None

    except Exception as e:
        print(f"❌ Error querying Ollama: {e}")
        return None
if __name__ == "__main__":
    service_name = infer_dependency_from_call(
        caller_service="service_a",
        method="POST",
        url="http://localhost:5001/api/pay"
    )

    print(f"📡 Inferred dependency: {service_name}")