# ============================================================
# Dockerfile - Santos Pegasus Soluciones RAG Agent
# ============================================================
# Imagen base liviana de Python
FROM python:3.11-slim

# ─── Etiquetas ──────────────────────────────────────────────
LABEL maintainer="Santos Pegasus Soluciones"
LABEL description="Agente RAG para documentacion tecnica interna"
LABEL version="1.0.0"

# ─── Evitar que Python genere archivos .pyc ────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ─── Directorio de trabajo ─────────────────────────────────
WORKDIR /app

# ─── Dependencias del sistema (mínimas) ────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ─── Instalar dependencias Python ──────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── Copiar código fuente ──────────────────────────────────
COPY src/ src/
COPY app.py .

# ─── Crear directorios para datos persistentes ─────────────
RUN mkdir -p /app/data/chroma_db /app/data/sessions

# ─── Puerto de Streamlit ───────────────────────────────────
EXPOSE 8501

# ─── Comando por defecto ───────────────────────────────────
# Streamlit se bindea a 0.0.0.0 para que sea accesible
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
