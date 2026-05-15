import requests
import json

# URL de tokens de producción
TOKEN_URL = "https://api.teamplace.finneg.com/api/oauth/token"
MCP_URL = "https://services.finneg.com/api/1/finnegans-developer-mcp/finnegans-api-docs/mcp"

# Credenciales de PROD (para el token)
CLIENT_ID_PROD = "859744933f6e25e17025da8a040b45cc"
CLIENT_SECRET_PROD = "aea5d0380ec3b6596f72071a94f23c0b"

# Credenciales de MCP (para los headers extra si hicieran falta)
CLIENT_ID_MCP = "e0f5a80bf36e8eb8a29a30de60b5985357473859130e8ce905c169d1b46f1eca81b12071a10878100a80e566e5e5df"

def test_go_token_flow():
    print("--- 1. Obteniendo Token de GO ---")
    params = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID_PROD,
        "client_secret": CLIENT_SECRET_PROD
    }
    
    try:
        resp = requests.get(TOKEN_URL, params=params, timeout=20)
        print(f"Status Token: {resp.status_code}")
        print(f"Respuesta Raw: {resp.text[:200]}")
        
        body_text = resp.text.strip()
        token = None
        # Intentar parsear como JSON primero, si falla, usar el texto directo
        try:
            data = resp.json()
            token = data.get("access_token")
        except:
            if " " not in body_text and len(body_text) > 10:
                token = body_text
        
        if not token:
            print(f"FAIL - No se pudo extraer el token. Respuesta: {body_text}")
            return

        print(f"SUCCESS - Token obtenido: {token[:10]}...")

        print("\n--- 2. Probando MCP con 'go-token' ---")
        # Según la documentación, se usa "go-token" como esquema de autorización
        headers = {
            "Authorization": f"go-token {token}",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "x-client-id": CLIENT_ID_MCP # Mantenemos el client-id por si acaso
        }
        
        # Primero intentamos un GET de SSE
        print(">>> Enviando GET (SSE) con go-token...")
        mcp_resp = requests.get(MCP_URL, headers=headers, stream=True, timeout=20)
        print(f"Status MCP (GET): {mcp_resp.status_code}")
        
        if mcp_resp.status_code == 200:
            print("🎉 ¡ÉXITO! Sesión iniciada con go-token.")
            for line in mcp_resp.iter_lines():
                if line: print(f"Evento: {line.decode('utf-8')}"); break
        else:
            print(f"Respuesta MCP: {mcp_resp.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_go_token_flow()
