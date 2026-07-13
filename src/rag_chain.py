"""
Cadena RAG (Retrieval-Augmented Generation) para Santos Pegasus Soluciones.
Soporta Cohere (default) y OpenRouter (fallback) como proveedores de LLM.
"""

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from src.config import (
    COMPANY_NAME,
    LLM_PROVIDER,
    COHERE_API_KEY,
    COHERE_CHAT_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    LLM_TEMPERATURE,
)

# ─── Prompt del sistema ─────────────────────────────────────────────
SYSTEM_PROMPT = f"""
Eres un asistente técnico especializado en la documentación interna de {COMPANY_NAME}.
Tu función es responder preguntas de desarrolladores, ingenieros y personal técnico
basándote EXCLUSIVAMENTE en los manuales y guías oficiales de la empresa.

DOCUMENTACIÓN DISPONIBLE:
- Arquitectura de Microservicios y Mapa de Dominios
- Manual de Onboarding para Nuevos Desarrolladores
- Protocolo de Respuesta a Incidentes y Post-Mortems (SRE)
- Guía Oficial de Ingeniería Back-end
- Guía Oficial de Ingeniería Front-end

INSTRUCCIONES:
1. Usá EXCLUSIVAMENTE el contexto proporcionado para responder. No inventes información.
2. Si la respuesta no se encuentra en el contexto, decí: "No tengo información sobre eso en la documentación de {COMPANY_NAME}."
3. Respondé SIEMPRE en español, de forma clara, técnica y profesional.
4. Si la pregunta incluye tecnologías, versiones o configuraciones específicas, verificá que coincidan exactamente con el contexto.
5. Citá el nombre del documento fuente cuando sea relevante (ej: "Según la Guía de Back-end...").

Contexto:
{{context}}
"""


def get_llm():
    """
    Retorna el modelo de lenguaje según el proveedor configurado.

    - cohere: usa ChatCohere (command-r-08-2024)
    - openrouter: usa ChatOpenRouter (modelo configurable, default: gemma gratis)
    """
    if LLM_PROVIDER == "cohere":
        if not COHERE_API_KEY:
            raise ValueError(
                "COHERE_API_KEY no está configurada. "
                "Creá un archivo .env o cambiá LLM_PROVIDER a 'openrouter'."
            )

        from langchain_cohere import ChatCohere

        print(f"[LLM] Usando Cohere: {COHERE_CHAT_MODEL}")
        return ChatCohere(
            model=COHERE_CHAT_MODEL,
            cohere_api_key=COHERE_API_KEY,
            temperature=LLM_TEMPERATURE,
        )

    else:
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY no está configurada. "
                "Creá un archivo .env con OPENROUTER_API_KEY=tu_key."
            )

        from langchain_openrouter import ChatOpenRouter

        print(f"[LLM] Usando OpenRouter: {OPENROUTER_MODEL}")
        return ChatOpenRouter(
            model=OPENROUTER_MODEL,
            api_key=OPENROUTER_API_KEY,
            temperature=LLM_TEMPERATURE,
        )


def create_rag_chain(retriever):
    """
    Crea la cadena RAG completa:
    1. Recupera los chunks más relevantes del vector store (retriever)
    2. Los inyecta en el prompt como contexto
    3. El LLM genera la respuesta final
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    print("[RAG] Cadena RAG creada correctamente")
    return rag_chain


def stream_answer(retriever, question: str):
    """
    Generador para streaming de respuesta RAG.
    Cada yield es un fragmento de texto del LLM (token a token).
    Después de agotar el generador, los docs recuperados quedan
    disponibles en stream_answer.docs y stream_answer.full_answer.
    """
    llm = get_llm()

    # 1. Recuperar contexto
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    # 2. Armar el prompt con el contexto inyectado
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])
    messages = prompt.format_messages(context=context, input=question)

    # 3. Streamear token a token
    full = ""
    for chunk in llm.stream(messages):
        content = getattr(chunk, "content", "")
        if content:
            full += content
            yield content

    # Guardar para que el caller pueda acceder después del streaming
    stream_answer.docs = docs
    stream_answer.full_answer = full


if __name__ == "__main__":
    # Prueba rápida de la cadena RAG
    from src.vector_store import get_retriever

    print("Inicializando retriever...")
    retriever = get_retriever()
    chain = create_rag_chain(retriever)

    pregunta = "¿Qué lenguajes de programación se usan en el back-end?"
    print(f"\nPregunta: {pregunta}")
    respuesta = chain.invoke({"input": pregunta})
    print(f"Respuesta: {respuesta['answer']}")
