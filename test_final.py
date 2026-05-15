import requests

# URL exacta de la documentación
URL_DOC = "https://services.finneg.com/api/1/finnegans-developer-mcp/finnegans-api-docs/mcp"
HEADERS = {
    "x-client-id": "e0f5a80bf36e8eb8a29a30de60b5985357473859130e8ce905c169d1b46f1eca81b12071a10878100a80e566e5e5df",
    "x-secret-key": "JDJhJDEwJFp2aWZsWFVqQUdjUnpQQjhSVnBrNk9kbzFTL1FKL2c2bGRTUlZtL2JidDJGbkNWTFJTRm1p",
    "Accept": "text/event-stream"
}

def test_final():
    # Según la documentación de MCP/SSE, el GET a la URL principal inicia el stream
    print(f"--- Prueba final GET SSE a la URL oficial ---")
    try:
        # Forzamos HTTPS y un timeout generoso
        response = requests.get(URL_DOC, headers=HEADERS, stream=True, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("!!! CONECTADO !!!")
            for line in response.iter_lines():
                if line: print(f"Data: {line.decode('utf-8')}"); break
        else:
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_final()
