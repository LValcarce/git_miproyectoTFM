FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar pandas y demás
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libatlas-base-dev \
    libpq-dev \
    curl \
    && apt-get clean

# Copia los archivos de la app
COPY . .

# Actualiza pip y wheel
RUN pip install --upgrade pip wheel setuptools

# Instala dependencias de Python (usa pandas binario)
RUN pip install --no-cache-dir pandas==2.2.2 \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD ["python", "app.py"]
