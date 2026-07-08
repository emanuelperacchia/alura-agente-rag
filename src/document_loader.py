"""
Carga y procesamiento de documentos PDF fuente.
Soporta carga de PDFs individuales o de directorios completos.
"""

import os
import glob

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import PDF_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_single_pdf(pdf_path: str) -> list:
    """
    Carga un único archivo PDF y devuelve una lista de documentos
    (uno por página) con su contenido y metadatos.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"  -> {os.path.basename(pdf_path)}: {len(documents)} paginas")
    return documents


def load_all_pdfs(pdf_dir: str = PDF_DIR) -> list:
    """
    Carga TODOS los archivos PDF de un directorio (búsqueda recursiva).
    Devuelve una lista combinada de documentos de todos los PDFs.
    """
    if not os.path.exists(pdf_dir):
        raise FileNotFoundError(
            f"No se encontró el directorio: {pdf_dir}\n"
            "Verificá que la ruta en PDF_DIR sea correcta."
        )

    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "**/*.pdf"), recursive=True))

    if not pdf_files:
        raise FileNotFoundError(
            f"No se encontraron archivos PDF en: {pdf_dir}"
        )

    print(f"[Loader] Buscando PDFs en: {pdf_dir}")
    print(f"[Loader] Archivos encontrados: {len(pdf_files)}")

    all_documents = []
    for pdf_path in pdf_files:
        docs = load_single_pdf(pdf_path)
        all_documents.extend(docs)

    print(f"[Loader] Total: {len(all_documents)} páginas combinadas")
    return all_documents


def split_documents(documents: list) -> list:
    """
    Divide los documentos en chunks superpuestos para mejorar
    la recuperación en el RAG.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"[Splitter] Documentos divididos en {len(chunks)} chunks")
    return chunks


def load_and_split(pdf_dir: str = PDF_DIR) -> list:
    """
    Función de conveniencia: carga todos los PDFs del directorio
    y los divide en chunks.
    """
    documents = load_all_pdfs(pdf_dir)
    chunks = split_documents(documents)
    return chunks
