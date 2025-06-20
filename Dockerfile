FROM python:3.11-slim

WORKDIR /app

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libatlas-base-dev \
    libpq-dev \
    curl \
    && apt-get clean

COPY . .

# Instala dependencias
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050
CMD ["gunicorn", "app:server"]

