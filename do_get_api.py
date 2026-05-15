import requests
import json

URL = "https://services.finneg.com/api/1/finnegans-developer-mcp/finnegans-api-docs/mcp"
CLIENT_ID = "e0f5a80bf36e8eb8a29a30de60b5985357473859130e8ce905c169d1b46f1eca81b12071a10878100a80e566e5e5df"
SECRET_KEY = "JDJhJDEwJFp2aWZsWFVqQUdjUnpQQjhSVnBrNk9kbzFTL1FKL2c2bGRTUlZtL2JidDJGbkNWTFJTRm1p"

def get_api_detail(api_id):
    headers = {
        "x-client-id": CLIENT_ID,
        "x-secret-key": SECRET_KEY,
        "Accept": "application/json, text/event-stream"
    }
    r_get = requests.get(URL, headers=headers, timeout=10)
    session_id = r_get.headers.get("mcp-session-id")
    
    headers["Content-Type"] = "application/json"
    headers["mcp-session-id"] = session_id
    
    # Initialize
    init_body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "debug", "version": "1.0.0"}
        }
    }
    requests.post(URL, json=init_body, headers=headers, timeout=15)
    
    # Get API
    call_body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_api",
            "arguments": {"api": api_id}
        }
    }
    r_call = requests.post(URL, json=call_body, headers=headers, timeout=15)
    
    print(f"Status: {r_call.status_code}")
    print(f"Response: {r_call.text}")

if __name__ == "__main__":
    get_api_detail("facturaVenta")
