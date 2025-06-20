FROM python:3.11-slim

WORKDIR /app

# Instala solo lo justo para evitar errores, pero sin sobreinstalar herramientas de build
RUN apt-get update && apt-get install -y \
    libatlas-base-dev \
    libpq-dev \
    curl \
    && apt-get clean

# Copia los archivos al contenedor
COPY . .

# Actualiza pip y wheel
RUN pip install --upgrade pip wheel setuptools

# Instala dependencias desde requirements.txt sin compilar (usa binarios)
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "app:server"]
