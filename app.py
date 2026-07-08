"""
Santos Pegasus Soluciones - Agente Inteligente RAG
Streamlit app con interfaz de chat para consultar documentación técnica.
"""

import streamlit as st

from src.config import COMPANY_NAME, LLM_PROVIDER

# ═══════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA (DEBE SER EL PRIMER COMANDO STREAMLIT)
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=f"{COMPANY_NAME} - Asistente Técnico",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════
# INICIALIZACIÓN DEL ESTADO DE SESIÓN
# ═══════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain_ready" not in st.session_state:
    st.session_state.chain_ready = False

if "error" not in st.session_state:
    st.session_state.error = None


# ═══════════════════════════════════════════════════════════════════
# BARRA LATERAL
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/software-engineer.png",
        width=80,
    )
    st.title(f"💻 {COMPANY_NAME}")
    st.caption("Asistente Técnico de Documentación")

    st.divider()

    st.subheader("ℹ️ Acerca de")
    st.markdown(
        f"""
        Este asistente utiliza **RAG (Retrieval-Augmented Generation)**
        para responder preguntas sobre la documentación técnica de
        **{COMPANY_NAME}**.

        **Documentación cargada:**
        - 🏗️ Arquitectura de Microservicios
        - 📚 Manual de Onboarding
        - 🚨 Protocolo de Incidentes (SRE)
        - ⚙️ Guía de Ingeniería Back-end
        - 🎨 Guía de Ingeniería Front-end
        """
    )

    st.divider()

    st.subheader("💡 Preguntas de ejemplo")
    st.markdown(
        """
        Hacé clic en una pregunta para copiarla:

        - ¿Qué lenguajes se usan en el back-end?
        - ¿Cómo es el proceso de onboarding?
        - ¿Qué hago ante un incidente crítico?
        - ¿Qué framework de front-end recomiendan?
        - ¿Cómo están organizados los microservicios?
        - ¿Qué es un post-mortem y cuándo se hace?
        """
    )

    st.divider()

    # Proveedor activo
    if LLM_PROVIDER == "cohere":
        provider_badge = "✅ Cohere (default)"
    else:
        provider_badge = "🔄 OpenRouter (fallback)"

    st.caption(f"**LLM activo:** {provider_badge}")

    # Botón para limpiar chat
    if st.button("🗑️ Limpiar conversación", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Botón para reinicializar (si hubo error)
    if st.session_state.error:
        if st.button("🔄 Reintentar conexión", type="primary", use_container_width=True):
            st.session_state.error = None
            st.session_state.chain_ready = False
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# INICIALIZACIÓN DE LA CADENA RAG (UNA SOLA VEZ)
# ═══════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="🔍 Preparando el asistente técnico...")
def init_rag_chain():
    """Inicializa el retriever y la cadena RAG (cacheado)."""
    from src.vector_store import get_retriever
    from src.rag_chain import create_rag_chain

    retriever = get_retriever()
    chain = create_rag_chain(retriever)
    return chain


if not st.session_state.chain_ready and not st.session_state.error:
    try:
        st.session_state.rag_chain = init_rag_chain()
        st.session_state.chain_ready = True
    except Exception as e:
        st.session_state.error = str(e)


# ═══════════════════════════════════════════════════════════════════
# ENCABEZADO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
st.title(f"💻 {COMPANY_NAME}")
st.markdown(
    "**Asistente Técnico de Documentación**  \n"
    "Consultame sobre microservicios, desarrollo, onboarding, incidentes y más."
)

st.divider()

# ═══════════════════════════════════════════════════════════════════
# MANEJO DE ERRORES DE INICIALIZACIÓN
# ═══════════════════════════════════════════════════════════════════
if st.session_state.error:
    st.error(
        f"❌ Error al inicializar el asistente:\n\n```\n{st.session_state.error}\n```\n\n"
        "**Posibles soluciones:**\n"
        "1. Verificá que el archivo `.env` tenga las API keys configuradas.\n"
        "2. Verificá que los PDFs estén en la carpeta correcta.\n"
        "3. Si usás OpenRouter, asegurate de tener saldo o elegí un modelo gratuito.\n"
        "4. Hacé clic en 'Reintentar conexión' en la barra lateral."
    )
    st.stop()

# ═══════════════════════════════════════════════════════════════════
# HISTORIAL DE CHAT
# ═══════════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ═══════════════════════════════════════════════════════════════════
# INPUT DEL USUARIO
# ═══════════════════════════════════════════════════════════════════
if question := st.chat_input(f"Escribí tu pregunta sobre la documentación de {COMPANY_NAME}..."):
    # Agregar pregunta al historial
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Obtener respuesta
    with st.chat_message("assistant"):
        with st.spinner("🔍 Buscando en la documentación..."):
            try:
                result = st.session_state.rag_chain.invoke({"input": question})
                answer = result["answer"]

                # Mostrar fuentes (metadata de los chunks recuperados)
                if "context" in result and result["context"]:
                    sources = set()
                    for doc in result["context"]:
                        source_info = doc.metadata.get("source", "")
                        page = doc.metadata.get("page", "")
                        if source_info:
                            sources.add(f"{source_info} (pág. {page})")

                    if sources:
                        source_text = "  \n*📄 Fuentes: " + ", ".join(sorted(sources)) + "*"
                        answer += "\n\n" + source_text

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                error_msg = f"❌ Error al procesar la pregunta: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})


# ═══════════════════════════════════════════════════════════════════
# MENSAJE INICIAL (si no hay historial)
# ═══════════════════════════════════════════════════════════════════
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown(
            f"¡Hola! 👋 Soy el asistente técnico de **{COMPANY_NAME}**.  \n\n"
            "Puedo ayudarte con preguntas sobre:  \n"
            "- 🏗️ **Arquitectura de Microservicios** y mapa de dominios  \n"
            "- 📚 **Onboarding** para nuevos desarrolladores  \n"
            "- 🚨 **Protocolo de Incidentes** y post-mortems  \n"
            "- ⚙️ **Guía de Ingeniería Back-end**  \n"
            "- 🎨 **Guía de Ingeniería Front-end**  \n\n"
            "¿En qué puedo ayudarte hoy?"
        )
