# Usamos una versión estable de Python
FROM python:3.10-slim

# Instalamos las librerías de sistema necesarias para PDF y compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo en el servidor
WORKDIR /app

# Copiamos e instalamos dependencias
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo tu código al servidor
COPY . .

# Comando para preparar los archivos estáticos (Bootstrap, CSS, etc.)
RUN python manage.py collectstatic --noinput

# Puerto que usa Render
EXPOSE 10000

# Comando para arrancar la aplicación
# IMPORTANTE: Asegúrate de que 'sistema_laboratorios' sea el nombre de tu carpeta principal
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "sistema_laboratorios.wsgi"]