# Usar una imagen ligera de Python
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY main.py .
COPY .env .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el bridge (con -u para unbuffered stdout)
ENTRYPOINT ["python", "-u", "main.py"]
