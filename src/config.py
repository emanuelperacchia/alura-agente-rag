"""
Configuración centralizada del agente Santos Pegasus Soluciones.
Soporta Cohere (default) y OpenRouter + HuggingFace como fallback.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── Empresa / Contexto ─────────────────────────────────────────────
COMPANY_NAME = "Santos Pegasus Soluciones"
COMPANY_DESCRIPTION = "Empresa de tecnología especializada en desarrollo de software escalable bajo arquitectura de microservicios"

# ─── Proveedor de LLM ──────────────────────────────────────────────
# Valores posibles: "cohere" | "openrouter"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "cohere")

# ─── Cohere ─────────────────────────────────────────────────────────
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

# Modelo de Cohere para chat
COHERE_CHAT_MODEL = os.getenv("COHERE_CHAT_MODEL", "command-r-08-2024")

# Modelo de Cohere para embeddings (multilingüe, ideal para español)
COHERE_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-multilingual-v3.0")

# ─── OpenRouter (fallback) ──────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemma-3n-e2b-it:free")

# Modelo de HuggingFace para embeddings (usado cuando LLM_PROVIDER = openrouter)
# all-MiniLM-L6-v2 es liviano (~80MB) y no requiere API key
HUGGINGFACE_EMBED_MODEL = os.getenv(
    "HUGGINGFACE_EMBED_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ─── Rutas de archivos ─────────────────────────────────────────────
# Directorio que contiene los PDFs de documentación
PDF_DIR = os.getenv("PDF_DIR", "../Docs/Santos Pegasus Soluciones/")

# Vector store persistente
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma_db")

# ─── Configuración del RAG ─────────────────────────────────────────
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "4"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
