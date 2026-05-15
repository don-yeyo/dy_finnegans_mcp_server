import os
import sys
import json
import requests
import logging
import uuid
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bridge.log"), logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("finnegans-bridge")

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
        logger.info(f"Sesión obtenida: {sid}")
        return sid
    except Exception as e:
        logger.error(f"Error obteniendo sesión: {e}")
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
    try:
        r = requests.post(URL, json=body, headers=headers, timeout=10)
        logger.info(f"Servidor inicializado: {r.status_code}")
    except Exception as e:
        logger.error(f"Error inicializando servidor: {e}")

SESSION_ID = get_session_id()
init_server(SESSION_ID)

def main():
    logger.info("Iniciando Super-Bridge con Anuncio de Herramientas...")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-client-id": CLIENT_ID,
        "x-secret-key": SECRET_KEY
    }

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            message = json.loads(line)
            method = message.get("method")
            params = message.get("params", {})
            
            if method == "list_tools" or method == "initialize":
                tools = [
                    {
                        "name": "search_code",
                        "description": "Buscador de APIs en Finnegans (Suplantado)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Texto a buscar"}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_file_contents",
                        "description": "Obtener detalle de una API (Suplantado)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "ID de la API"}
                            },
                            "required": ["path"]
                        }
                    }
                ]
                
                if method == "initialize":
                    resp = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {}},
                            "serverInfo": {"name": "github-mcp-server", "version": "1.0.0"}
                        }
                    }
                else: # list_tools
                    resp = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": {"tools": tools}
                    }
                
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                continue

            if method == "tools/call":
                tool_name = params.get("name")
                mcp_args = params.get("arguments", {})
                
                if tool_name == "search_code":
                    new_method = "search_apis"
                    new_params = {"query": mcp_args.get("query")}
                elif tool_name == "get_file_contents":
                    new_method = "get_api"
                    new_params = {"api": mcp_args.get("path")}
                else:
                    new_method = tool_name
                    new_params = mcp_args

                body = {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "method": "tools/call",
                    "params": {
                        "name": new_method,
                        "arguments": new_params
                    }
                }
                
                headers["mcp-session-id"] = SESSION_ID
                target_url = URL
                r = requests.post(target_url, json=body, headers=headers, timeout=15)
                
                response_text = r.text
                if "data: " in response_text:
                    for resp_line in response_text.split("\n"):
                        if resp_line.startswith("data: "):
                            response_text = resp_line.replace("data: ", "").strip()
                            break
                
                logger.info(f"Respuesta final procesada: {response_text}")
                sys.stdout.write(response_text + "\n")
                sys.stdout.flush()
                continue

        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
