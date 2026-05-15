import requests
import json
import sys
import time

URL = "https://services.finneg.com/api/1/finnegans-developer-mcp/finnegans-api-docs/mcp"
HEADERS = {
    "x-client-id": "e0f5a80bf36e8eb8a29a30de60b5985357473859130e8ce905c169d1b46f1eca81b12071a10878100a80e566e5e5df",
    "x-secret-key": "JDJhJDEwJFp2aWZsWFVqQUdjUnpQQjhSVnBrNk9kbzFTL1FKL2c2bGRTUlZtL2JidDJGbkNWTFJTRm1p",
    "Accept": "text/event-stream"
}

def search(query):
    print(f"Buscando '{query}' en Finnegans...")
    try:
        # 1. Abrimos el canal SSE (GET)
        print(">>> Conectando al canal de eventos...")
        with requests.get(URL, headers=HEADERS, stream=True, timeout=30) as sse_resp:
            print(f"Status: {sse_resp.status_code}")
            session_id = None
            for line in sse_resp.iter_lines():
                if line:
                    decoded = line.decode('utf-8').strip()
                    print(f"Recibido: {decoded}")
                    if decoded.startswith("data:"):
                        session_id = decoded[5:].strip()
                        print(f"ID Detectado: {session_id}")
                        break
                else:
                    print("(Línea vacía)")
            
            if not session_id:
                print("FAIL - El servidor no envió ningún evento de datos.")
                return

            # 2. Ahora que tenemos la sesión, hacemos el POST
            # La respuesta de Finnegans suele dar una URL completa o un ID
            if session_id.startswith("http"):
                post_url = session_id
            else:
                post_url = f"{URL}?sessionId={session_id}"

            post_headers = HEADERS.copy()
            post_headers["Content-Type"] = "application/json"
            post_headers["Accept"] = "application/json"
            
            body = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "search_apis",
                "params": {"query": query}
            }
            
            r = requests.post(post_url, json=body, headers=post_headers)
            if r.status_code == 200:
                print(json.dumps(r.json(), indent=2, ensure_ascii=False))
            else:
                print(f"Error en consulta: {r.status_code} - {r.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search(sys.argv[1])
