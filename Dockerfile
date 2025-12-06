# Dockerfile para Detector de Plagio
# Uso: docker build -t detector-plagio .
#      docker run -p 8501:8501 detector-plagio

FROM python:3.9-slim

# Metadata
LABEL maintainer="Alma Paulina González Sandoval, Diego Sánchez Valle"
LABEL description="Detector de Plagio con Análisis Multidimensional usando Streamlit"
LABEL version="1.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para cachear layer)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelos de spaCy
RUN python -m spacy download es_core_news_md

# Copiar el resto del código
COPY . .

# Crear directorio de cache
RUN mkdir -p /app/cache

# Exponer puerto de Streamlit
EXPOSE 8501

# Healthcheck para verificar que la app está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=true"]
