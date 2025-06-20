FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Instalar dependencias del sistema necesarias para pandas, plotly, etc.
RUN apt-get update && apt-get install -y build-essential gcc g++ libpq-dev curl

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD ["python", "app.py"]
