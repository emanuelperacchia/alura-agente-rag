"""
Manejo del vector store con Chroma.
Soporta Cohere Embeddings (default) y HuggingFace Embeddings (fallback).
"""

import os
import shutil

from langchain_chroma import Chroma

from src.config import (
    LLM_PROVIDER,
    COHERE_API_KEY,
    COHERE_EMBED_MODEL,
    HUGGINGFACE_EMBED_MODEL,
    CHROMA_PATH,
    RETRIEVER_K,
)


def get_embeddings():
    """
    Retorna el modelo de embeddings según el proveedor de LLM configurado.

    - cohere: usa CohereEmbeddings (multilingüe, ideal para español)
    - openrouter: usa HuggingFaceEmbeddings (gratuito, local, ~80MB)
    """
    if LLM_PROVIDER == "cohere":
        from langchain_cohere import CohereEmbeddings

        if not COHERE_API_KEY:
            raise ValueError(
                "COHERE_API_KEY no está configurada. "
                "Creá un archivo .env con COHERE_API_KEY=tu_key o "
                "cambiá LLM_PROVIDER a 'openrouter'."
            )

        print(f"[Embeddings] Usando Cohere: {COHERE_EMBED_MODEL}")
        return CohereEmbeddings(
            model=COHERE_EMBED_MODEL,
            cohere_api_key=COHERE_API_KEY,
        )

    else:
        from langchain_huggingface import HuggingFaceEmbeddings

        print(f"[Embeddings] Usando HuggingFace: {HUGGINGFACE_EMBED_MODEL}")
        return HuggingFaceEmbeddings(
            model_name=HUGGINGFACE_EMBED_MODEL,
        )


def _create_vector_store(documents: list, embeddings) -> Chroma:
    """
    Crea un nuevo vector store a partir de los documentos chunkeados.
    Si ya existe uno, lo elimina y lo recrea.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"[VectorStore] Directorio existente eliminado: {CHROMA_PATH}")

    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )
    print(f"[VectorStore] Vector store creado en: {CHROMA_PATH}")
    return db


def _load_vector_store(embeddings) -> Chroma:
    """
    Carga un vector store existente desde disco.
    """
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(
            f"No se encontró el vector store en {CHROMA_PATH}. "
            "Ejecutá primero 'python -c \"from src.vector_store import build_vector_store; build_vector_store()\"'"
        )

    db = Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
    )
    print(f"[VectorStore] Vector store cargado desde: {CHROMA_PATH}")
    return db


def build_vector_store(documents: list = None):
    """
    Construye el vector store desde cero.
    Si no se pasan documentos, los carga y divide automáticamente.
    """
    if documents is None:
        from src.document_loader import load_and_split
        documents = load_and_split()

    embeddings = get_embeddings()
    db = _create_vector_store(documents, embeddings)
    return db


def get_retriever(documents: list = None):
    """
    Retorna un retriever configurado.
    Si se pasan documentos, construye el vector store desde cero.
    Si no, intenta cargar uno existente.
    """
    from src.document_loader import load_and_split

    if documents is None and not os.path.exists(CHROMA_PATH):
        print("[Retriever] Vector store no encontrado. Construyendo desde cero...")
        documents = load_and_split()

    embeddings = get_embeddings()

    if documents:
        db = _create_vector_store(documents, embeddings)
    else:
        db = _load_vector_store(embeddings)

    retriever = db.as_retriever(
        search_kwargs={"k": RETRIEVER_K}
    )
    print(f"[Retriever] Retriever configurado (top-{RETRIEVER_K} chunks)")
    return retriever
