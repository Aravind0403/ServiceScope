import httpx

def generate_report():
    resp = httpx.get("http://reporting-service/api/metrics")
    return resp.json()