import json
import subprocess
import time

def test_bridge():
    # Mensaje estándar de inicialización de MCP
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }

    print("--- Iniciando prueba del bridge ---")
    
    # Ejecutar el bridge localmente
    process = subprocess.Popen(
        ["python", "-u", "C:/Users/gabrielt/Documents/Finnegans/dy_finnegans_mcp_server/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # Enviar initialize
        print(">>> Enviando 'initialize'...")
        process.stdin.write(json.dumps(init_message) + "\n")
        process.stdin.flush()

        # Leer respuesta
        print("<<< Esperando respuesta...")
        line = process.stdout.readline()
        if line:
            print(f"OK - Respuesta recibida: {line[:200]}...")
            resp = json.loads(line)
            if "error" in resp:
                print(f"ERROR - El servidor devolvió un error: {resp['error']}")
            else:
                print("SUCCESS - El servidor respondió correctamente con sus capacidades.")
        else:
            err = process.stderr.read()
            print(f"FAIL - No hubo respuesta por stdout. Error en stderr: {err}")

    except Exception as e:
        print(f"FAIL - Error durante la prueba: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    test_bridge()
