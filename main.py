import os
import sys
import json
import requests
import logging
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bridge.log"),
        logging.StreamHandler(sys.stderr) # Los logs van a stderr para no interferir con stdout (JSON-RPC)
    ]
)
logger = logging.getLogger("finnegans-bridge")

# Cargar variables de entorno
load_dotenv()

URL = os.getenv("FINNEGANS_MCP_URL")
CLIENT_ID = os.getenv("FINNEGANS_CLIENT_ID")
SECRET_KEY = os.getenv("FINNEGANS_SECRET_KEY")

def main():
    if not all([URL, CLIENT_ID, SECRET_KEY]):
        logger.error("Faltan variables de entorno en el archivo .env")
        sys.exit(1)

    logger.info(f"Bridge iniciado. Conectando a {URL}")

    # Headers requeridos por Finnegans
    headers = {
        "Content-Type": "application/json",
        "x-client-id": CLIENT_ID,
        "x-secret-key": SECRET_KEY
    }

    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            
            try:
                # 1. Recibir mensaje JSON-RPC desde el host (Antigravity/Claude)
                message = json.loads(line)
                logger.debug(f"Mensaje recibido: {message.get('method')}")

                # 2. Reenviar al servidor remoto de Finnegans
                response = requests.post(URL, json=message, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    # 3. Devolver la respuesta al host por stdout
                    sys.stdout.write(response.text + "\n")
                    sys.stdout.flush()
                else:
                    logger.error(f"Error remoto: {response.status_code} - {response.text}")
                    # Enviar un error JSON-RPC de vuelta si el remoto falla
                    error_resp = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "error": {
                            "code": -32000,
                            "message": f"Remote Finnegans server error: {response.status_code}"
                        }
                    }
                    sys.stdout.write(json.dumps(error_resp) + "\n")
                    sys.stdout.flush()

            except json.JSONDecodeError:
                logger.error(f"Error al decodificar JSON de la entrada: {line}")
            except Exception as e:
                logger.error(f"Error procesando mensaje: {str(e)}")
                # Intentar enviar error al host
                try:
                    error_id = message.get("id") if 'message' in locals() else None
                    error_resp = {
                        "jsonrpc": "2.0",
                        "id": error_id,
                        "error": {"code": -32603, "message": str(e)}
                    }
                    sys.stdout.write(json.dumps(error_resp) + "\n")
                    sys.stdout.flush()
                except:
                    pass

    except KeyboardInterrupt:
        logger.info("Bridge detenido por el usuario.")

if __name__ == "__main__":
    main()
