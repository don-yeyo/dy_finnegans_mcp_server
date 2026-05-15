import requests
import json

URL = "https://services.finneg.com/api/1/finnegans-developer-mcp/finnegans-api-docs/mcp"
HEADERS = {
    "x-client-id": "e0f5a80bf36e8eb8a29a30de60b5985357473859130e8ce905c169d1b46f1eca81b12071a10878100a80e566e5e5df",
    "x-secret-key": "JDJhJDEwJFp2aWZsWFVqQUdjUnpQQjhSVnBrNk9kbzFTL1FKL2c2bGRTUlZtL2JidDJGbkNWTFJTRm1p",
    "Accept": "text/event-stream"
}

def discover():
    print(f"--- Intentando con POST para iniciar sesión ---")
    try:
        response = requests.post(URL, headers=HEADERS, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                print(f"Recibido: {decoded}")
                # Buscamos algo que parezca un endpoint o sessionId
                if "endpoint" in decoded or "sessionId" in decoded:
                    print("!!! ENCONTRADO POSIBLE ID !!!")
                    break
            if response.status_code != 200: break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    discover()
