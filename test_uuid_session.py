import requests
import json
import uuid

URL = "https://services.finneg.com/api/1/finnegans-developer-mcp/finnegans-api-docs/mcp"
# Generamos un ID de sesión único para esta prueba
SESSION_ID = str(uuid.uuid4())

HEADERS = {
    "x-client-id": "e0f5a80bf36e8eb8a29a30de60b5985357473859130e8ce905c169d1b46f1eca81b12071a10878100a80e566e5e5df",
    "x-secret-key": "JDJhJDEwJFp2aWZsWFVqQUdjUnpQQjhSVnBrNk9kbzFTL1FKL2c2bGRTUlZtL2JidDJGbkNWTFJTRm1p",
    "Accept": "text/event-stream",
    "Content-Type": "application/json"
}

def test_session():
    # Añadimos el sessionId a la URL
    test_url = f"{URL}?sessionId={SESSION_ID}"
    print(f"--- Probando con SessionID autogenerado: {SESSION_ID} ---")
    print(f"URL: {test_url}")
    
    try:
        # 1. Intentar el GET para abrir el canal SSE
        print(">>> Enviando GET (SSE)...")
        response = requests.get(test_url, headers=HEADERS, stream=True, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 ¡CONEXIÓN EXITOSA! Leyendo eventos...")
            for line in response.iter_lines():
                if line:
                    print(f"Evento: {line.decode('utf-8')}")
                    break # Con uno basta para validar
        else:
            print(f"Fallo: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_session()
