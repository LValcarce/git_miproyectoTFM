# Usa una imagen oficial con Python 3.11
FROM python:3.11-slim

# Crea directorio para la app
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto por defecto de Dash
EXPOSE 8050

# Comando para ejecutar la app
CMD ["python", "app.py"]
