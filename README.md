# Finnegans MCP Bridge Server

Este proyecto actúa como un puente (proxy) local para el servidor MCP de Finnegans que se encuentra alojado de forma remota. Permite que asistentes de IA (como Antigravity) interactúen con la API de Finnegans utilizando el protocolo estándar MCP sobre `stdio`.

## Requisitos

- Python 3.9+
- Dependencias: `requests`, `python-dotenv`

## Instalación

1. Clona este repositorio o copia los archivos.
2. Instala las dependencias:
   ```bash
   pip install requests python-dotenv
   ```
3. Configura tus credenciales en el archivo `.env` (usa `.env.template` como base).

## Configuración en el Agente (mcp_config.json)

Para integrar este servidor, añade la siguiente configuración a tu archivo `mcp_config.json`:

```json
"finnegans": {
  "command": "python",
  "args": ["C:/Users/gabrielt/Documents/Finnegans/dy_finnegans_mcp_server/main.py"],
  "env": {
    "PYTHONPATH": "C:/Users/gabrielt/Documents/Finnegans/dy_finnegans_mcp_server"
  }
}
```

## Funcionalidades

- Traduce peticiones `stdio` JSON-RPC a peticiones `HTTP POST` hacia el servidor de Finnegans.
- Maneja la autenticación mediante headers `x-client-id` y `x-secret-key`.
- Proporciona logs de depuración en `bridge.log`.
