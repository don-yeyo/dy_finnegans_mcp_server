import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("FINNEGANS_MCP_URL")
CLIENT_ID = os.getenv("FINNEGANS_CLIENT_ID")
SECRET_KEY = os.getenv("FINNEGANS_SECRET_KEY")

def get_session_id():
    headers = {
        "x-client-id": CLIENT_ID,
        "x-secret-key": SECRET_KEY,
        "Accept": "application/json, text/event-stream"
    }
    try:
        r = requests.get(URL, headers=headers, timeout=10)
        sid = r.headers.get("mcp-session-id")
        return sid
    except Exception as e:
        print(f"Error obteniendo sesión: {e}")
        return None

def init_server(sid):
    if not sid: return
    headers = {
        "x-client-id": CLIENT_ID,
        "x-secret-key": SECRET_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": sid
    }
    body = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "finnegans-bridge", "version": "1.0.0"}
        }
    }
    requests.post(URL, json=body, headers=headers, timeout=10)

def search_apis(query):
    sid = get_session_id()
    if not sid:
        print("No se pudo obtener el Session ID.")
        return
    
    init_server(sid)

    headers = {
        "x-client-id": CLIENT_ID,
        "x-secret-key": SECRET_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": sid
    }

    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "get_api",
            "arguments": {"api": "REMITOSVINCULADOSALPEDIDOAPI"}
        }
    }

    try:
        r = requests.post(URL, json=body, headers=headers, timeout=15)
        print(f"Status Code: {r.status_code}")
        with open("search_results.json", "w", encoding="utf-8") as f:
            f.write(r.text)
        print("Resultados guardados en search_results.json")
    except Exception as e:
        print(f"Error en la petición: {e}")

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "clientes"
    search_apis(query)
