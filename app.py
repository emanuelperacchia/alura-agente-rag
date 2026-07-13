"""
Santos Pegasus Soluciones - Asistente Técnico RAG
Chat inteligente sobre documentación técnica interna.
Design System: verde #00E28A · verde oscuro #071A14 · tipografía Roobert/Inter
"""

import json
import uuid
from pathlib import Path

import streamlit as st

from src.config import COMPANY_NAME, LLM_PROVIDER

# ─── Sesión persistente en archivos locales ────────────────
SESSIONS_DIR = Path("data/sessions")
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def _session_path(sid: str) -> Path:
    return SESSIONS_DIR / f"{sid}.json"


def _load_session(sid: str) -> list:
    p = _session_path(sid)
    if p.exists():
        try:
            return json.loads(p.read_text("utf-8")).get("messages", [])
        except Exception:
            return []
    return []


def _save_session(sid: str, messages: list):
    _session_path(sid).write_text(
        json.dumps({"messages": messages}, ensure_ascii=False), "utf-8"
    )


def _clear_session(sid: str):
    p = _session_path(sid)
    if p.exists():
        p.unlink()

# Avatares del chat
AVATAR_USER = "👤"
AVATAR_ASSISTANT = "🪽"

# ═══════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=f"{COMPANY_NAME} - Asistente Técnico",
    page_icon="🪽",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════
# CSS — Design System Santos Pegasus
# Fondos y textos base → Streamlit via .streamlit/config.toml
# Variables + selectores para elementos custom
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --green-400: #00E28A;
        --green-900: #071A14;
        --font-brand: "Inter", system-ui, sans-serif;
    }

    /* Streamlit provee --text-color, --background-color, --secondary-background-color
       que se actualizan solas al togglear tema. Las usamos en vez de [data-theme]. */

    /* ── Brand ── */
    .brand-logo {
        background: linear-gradient(135deg, #00E28A 0%, #0A6650 100%) !important;
        box-shadow: 0 0 0 2px rgba(0,226,138,0.2);
        display: flex; align-items: center; justify-content: center;
        width: 52px; height: 52px;
        border-radius: 14px; font-weight: 700; font-size: 1.2rem;
        color: white !important; flex-shrink: 0;
    }
    .brand-header {
        display: flex; align-items: center; gap: 1rem;
        padding: 1.5rem 0 0.5rem 0; margin-bottom: 0.5rem;
    }
    .brand-text { line-height: 1.2; }
    .brand-name {
        font-size: 1.8rem; font-weight: 700; letter-spacing: -0.02em; margin: 0;
        color: var(--text-color) !important;
    }
    .brand-tagline { font-size: 0.85rem; margin: 0; line-height: 1.5; color: var(--text-color) !important; opacity: 0.65; }
    .brand-badge {
        display: inline-block; font-size: 0.65rem; font-weight: 700;
        color: #071A14 !important;
        background: #00E28A !important;
        padding: 0.15rem 0.6rem; border-radius: 999px;
        margin-left: 0.5rem; vertical-align: middle; letter-spacing: 0.03em;
    }

    /* ── Animaciones ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .stChatMessage {
        animation: fadeInUp 0.3s ease-out !important;
        padding: 0.75rem 1rem !important;
        border-radius: 12px !important;
        margin-bottom: 0.75rem !important;
        transition: box-shadow 0.2s ease !important;
    }
    .stChatMessage:hover {
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }
    [data-testid="chat-user-message"] {
        background: linear-gradient(135deg, #00E28A 0%, #0A6650 100%) !important;
        color: #FFFFFF !important;
    }
    [data-testid="chat-user-message"] p { color: #FFFFFF !important; }
    [data-testid="chat-assistant-message"] { background: var(--secondary-background-color) !important; }

    /* ── Welcome grid ── */
    .welcome-grid {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 0.4rem; margin: 0.5rem 0;
    }
    .welcome-item {
        display: flex; align-items: center; gap: 0.5rem;
        padding: 0.4rem 0.6rem;
        border-radius: 8px;
        background: var(--background-color) !important;
        border: 1px solid var(--text-color); border-opacity: 0.1;
        animation: fadeIn 0.5s ease-out;
    }
    .welcome-icon { font-size: 1.1rem; flex-shrink: 0; }
    .welcome-label { font-size: 0.8rem; font-weight: 600; color: var(--text-color) !important; }
    .welcome-desc { font-size: 0.68rem; color: var(--text-color) !important; opacity: 0.6; display: block; }

    /* ── Source cards (glassmorphism) ── */
    .source-card {
        border-radius: 8px; padding: 0.5rem 0.75rem; margin: 0.35rem 0;
        font-size: 0.78rem;
        border-left: 3px solid #00E28A !important;
        color: var(--text-color) !important; opacity: 0.85;
        background: var(--background-color) !important;
        backdrop-filter: blur(4px);
        transition: all 0.2s ease;
    }
    .source-card:hover {
        opacity: 1; border-left-width: 4px;
    }
    .source-card strong { color: var(--text-color) !important; opacity: 1; }
    .source-header { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.3rem; color: var(--text-color) !important; opacity: 0.65; }

    /* ── Sidebar ── */
    .sidebar-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-color) !important; opacity: 0.65; }
    section[data-testid="stSidebar"] .stButton button {
        border-radius: 8px !important; padding: 0.4rem 0.75rem !important;
        font-size: 0.82rem !important; transition: all 0.15s !important;
        line-height: 1.5 !important; width: 100% !important; text-align: left !important;
        background: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        border-color: #00E28A !important;
        transform: translateX(2px);
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        font-weight: 600 !important; text-align: center !important;
    }
    section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        background: var(--green-400) !important;
        transform: translateX(0) !important;
    }

    /* ── Stats ── */
    .stat-card { padding: 0.75rem; text-align: center; border-radius: 10px; background: var(--background-color) !important; }
    .stat-card .stat-value { font-size: 1.4rem; font-weight: 700; color: #00E28A !important; }
    .stat-card .stat-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-color) !important; opacity: 0.65; }

    /* ── Footer ── */
    .app-footer { text-align: center; padding: 1.5rem 0 0.5rem 0; font-size: 0.72rem; margin-top: 2rem; color: var(--text-color) !important; opacity: 0.5; }
    .app-footer span { margin: 0 0.4rem; }

    /* ── Spinner ── */
    .stSpinner > div > div { border-top-color: #00E28A !important; }

    /* ── Font (solo contenido, NO componentes Streamlit) ── */
    .brand-header, .brand-logo, .brand-text, .brand-name, .brand-tagline, .brand-badge,
    .stat-card, .stat-value, .stat-label, .sidebar-label,
    .source-card, .source-card strong, .source-header,
    .app-footer,
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stChatMessage, [data-testid*="chat"] {
        font-family: var(--font-brand) !important;
    }

    /* ── Error / alert ── */
    .stAlert, .stException, [data-testid="stNotification"], .st-bv {
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        white-space: pre-wrap !important;
    }
    .stAlert code, .stException code {
        font-size: 0.78rem !important;
        word-break: break-all !important;
    }

    /* ── Sidebar doc list ── */
    .doc-item { padding: 0.25rem 0; font-size: 0.85rem; }
    .doc-item strong { color: var(--text-color) !important; }
    .doc-item span { font-size: 0.75rem; color: var(--text-color) !important; opacity: 0.65; }

    /* ── Sidebar LLM ── */
    .llm-indicator { font-size: 0.78rem; color: var(--text-color) !important; }
    .llm-dot { color: #00E28A !important; }
    .llm-info { font-size: 0.68rem; color: var(--text-color) !important; opacity: 0.65; }

    /* ── Sidebar brand ── */
    .sb-title { font-size: 1.05rem; font-weight: 700; color: var(--text-color) !important; }
    .sb-sub { font-size: 0.72rem; color: var(--text-color) !important; opacity: 0.65; letter-spacing: 0.04em; }
    .sb-desc { font-size: 0.85rem; color: var(--text-color) !important; opacity: 0.65; margin-top: 0; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# ESTADO DE SESIÓN — persistente via URL + archivos locales
# ═══════════════════════════════════════════════════════════════════
if "session_id" not in st.session_state:
    sid = st.query_params.get("session")
    if not sid:
        sid = str(uuid.uuid4())
        st.query_params["session"] = sid
    st.session_state.session_id = sid
    st.session_state.messages = _load_session(sid)
else:
    if "messages" not in st.session_state:
        st.session_state.messages = _load_session(st.session_state.session_id)

if "chain_ready" not in st.session_state:
    st.session_state.chain_ready = False
if "error" not in st.session_state:
    st.session_state.error = None

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.75rem; margin: 0.5rem 0 0.25rem 0;">
        <div style="display:flex; align-items:center; justify-content:center;
            width:44px; height:44px;
            background:linear-gradient(135deg, #00E28A 0%, #0A6650 100%);
            border-radius:12px; font-weight:700; font-size:1.1rem;
            color:white; flex-shrink:0;
            box-shadow:0 0 0 2px rgba(0,226,138,0.15);">SP</div>
        <div style="line-height:1.15;">
            <div class="sb-title">Santos Pegasus</div>
            <div class="sb-sub">SOLUCIONES</div>
        </div>
    </div>
    <p class="sb-desc">Asistente Técnico</p>
    """, unsafe_allow_html=True)

    st.divider()

    # Stats
    col1, col2 = st.columns(2)
    col1.markdown('<div class="stat-card"><div class="stat-value">5</div><div class="stat-label">Documentos</div></div>', unsafe_allow_html=True)
    col2.markdown('<div class="stat-card"><div class="stat-value">152</div><div class="stat-label">Páginas</div></div>', unsafe_allow_html=True)

    st.divider()

    # Documentos
    st.markdown('<p class="sidebar-label">Documentación</p>', unsafe_allow_html=True)
    for icon, t, d in [
        ("🏗️", "Microservicios", "Arquitectura y mapa de dominios"),
        ("📚", "Onboarding", "Guía para nuevos desarrolladores"),
        ("🚨", "Incidentes", "Protocolo SRE y post-mortems"),
        ("⚙️", "Back-end", "Java, Spring Boot, APIs"),
        ("🎨", "Front-end", "React, componentes, testing"),
    ]:
        st.markdown(f'<div class="doc-item"><strong>{icon} {t}</strong><br><span>{d}</span></div>', unsafe_allow_html=True)

    st.divider()

    # Preguntas — como st.button nativo en lugar de raw HTML con JS
    st.markdown('<p class="sidebar-label">Preguntas frecuentes</p>', unsafe_allow_html=True)
    for q in [
        "¿Qué lenguajes se usan en el back-end?",
        "¿Cómo es el proceso de onboarding?",
        "¿Qué hago ante un incidente crítico?",
        "¿Qué framework de front-end recomiendan?",
        "¿Cómo están organizados los microservicios?",
        "¿Qué es un post-mortem y cuándo se hace?",
    ]:
        if st.button(q, key=f"q_{q[:20]}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

    st.divider()

    # Provider
    st.markdown(
        '<div class="llm-indicator">'
        '<span class="llm-dot">●</span> '
        '<strong>LLM activo:</strong><br>'
        '<span class="llm-info">Cohere — command-r + embed-multilingual-v3</span></div>',
        unsafe_allow_html=True,
    )


    st.divider()
    if st.button("🗑️ Nueva conversación", type="secondary", use_container_width=True):
        st.session_state.messages = []
        _clear_session(st.session_state.session_id)
        st.rerun()
    if st.session_state.error:
        if st.button("🔄 Reintentar conexión", type="primary", use_container_width=True):
            st.session_state.error = None
            st.session_state.chain_ready = False
            st.rerun()

# ═══════════════════════════════════════════════════════════════════
# RAG CHAIN (cacheada)
# ═══════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="🔍 Preparando el asistente técnico...")
def init_resources():
    """Inicializa y cachea el retriever y el RAG chain."""
    from src.vector_store import get_retriever
    from src.rag_chain import create_rag_chain
    retriever = get_retriever()
    chain = create_rag_chain(retriever)
    return retriever, chain

if not st.session_state.chain_ready and not st.session_state.error:
    try:
        st.session_state.retriever, st.session_state.rag_chain = init_resources()
        st.session_state.chain_ready = True
    except Exception as e:
        st.session_state.error = str(e)

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="brand-header">'
    f'<div class="brand-logo">SP</div>'
    f'<div class="brand-text">'
    f'<div class="brand-name">{COMPANY_NAME}<span class="brand-badge">RAG</span></div>'
    f'<div class="brand-tagline">Asistente Técnico de Documentación — consultame sobre microservicios, desarrollo, onboarding, incidentes y más.</div>'
    f'</div></div>',
    unsafe_allow_html=True,
)

# Error
if st.session_state.error:
    st.error(f"**Error al inicializar el asistente**  \n\n`{st.session_state.error}`  \n\n**Posibles soluciones:**  \n1. Verificá que el `.env` tenga las API keys  \n2. Verificá que los PDFs estén en la carpeta correcta  \n3. Si usás OpenRouter, asegurate de tener saldo  \n4. Hacé clic en 'Reintentar conexión' en la barra lateral")
    st.stop()

# ═══════════════════════════════════════════════════════════════════
# CHAT
# ═══════════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    avatar = AVATAR_ASSISTANT if msg["role"] == "assistant" else AVATAR_USER
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ─── Helper: generar respuesta con streaming ────────────────
def _respond(question: str):
    """Muestra la respuesta del asistente en streaming + fuentes."""
    from src.rag_chain import stream_answer

    with st.chat_message("assistant", avatar=AVATAR_ASSISTANT):
        status = st.status("🔍 Buscando en la documentación...", state="running")
        generator = stream_answer(st.session_state.retriever, question)
        response = st.write_stream(generator)
        status.update(label="✅ Respuesta generada", state="complete", expanded=False)

        # Fuentes
        if hasattr(stream_answer, "docs") and stream_answer.docs:
            seen = set()
            parts = ['<div style="margin-top:0.75rem;"><p class="source-header">📄 Fuentes consultadas</p>']
            for doc in stream_answer.docs:
                src, pg = doc.metadata.get("source", ""), doc.metadata.get("page", "")
                key = f"{src}|{pg}"
                if key not in seen and src:
                    seen.add(key)
                    fn = src.split("\\")[-1].split("/")[-1]
                    parts.append(f'<div class="source-card"><strong>{fn}</strong><span style="float:right;">pág. {pg}</span></div>')
            parts.append("</div>")
            st.markdown("".join(parts), unsafe_allow_html=True)

        full = stream_answer.full_answer if hasattr(stream_answer, "full_answer") else response
        st.session_state.messages.append({"role": "assistant", "content": full})
        _save_session(st.session_state.session_id, st.session_state.messages)

# ─── Procesar pregunta ─────────────────────────────────────
question = st.chat_input("Hacé tu pregunta sobre la documentación técnica...", max_chars=1000)

if question:
    # Pregunta escrita en el chat
    st.session_state.messages.append({"role": "user", "content": question})
    _save_session(st.session_state.session_id, st.session_state.messages)
    with st.chat_message("user", avatar=AVATAR_USER):
        st.markdown(question)
    _respond(question)

elif st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Pregunta desde botón predefinido (último msg sin respuesta)
    last_q = st.session_state.messages[-1]["content"]
    _respond(last_q)

# ═══════════════════════════════════════════════════════════════════
# FOOTER + WELCOME
# ═══════════════════════════════════════════════════════════════════
st.markdown(f'<div class="app-footer"><span>© {COMPANY_NAME}</span><span>·</span><span>RAG Agent</span><span>·</span><span>LangChain + Cohere</span><span>·</span><span>v1.0</span></div>', unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar=AVATAR_ASSISTANT):
        st.markdown(
            f"¡Hola! 👋 Soy el asistente técnico de **{COMPANY_NAME}**.  \n\n"
            "Tengo cargada toda la documentación técnica de la empresa. "
            "Hacé cualquier pregunta sobre:  \n\n"
            f"<div class='welcome-grid'>"
            f"<div class='welcome-item'><span class='welcome-icon'>🏗️</span><span class='welcome-label'>Microservicios</span><span class='welcome-desc'>Arquitectura, dominios, squads</span></div>"
            f"<div class='welcome-item'><span class='welcome-icon'>📚</span><span class='welcome-label'>Onboarding</span><span class='welcome-desc'>Guía para nuevos devs</span></div>"
            f"<div class='welcome-item'><span class='welcome-icon'>🚨</span><span class='welcome-label'>Incidentes</span><span class='welcome-desc'>Protocolo SRE, post-mortems</span></div>"
            f"<div class='welcome-item'><span class='welcome-icon'>⚙️</span><span class='welcome-label'>Back-end</span><span class='welcome-desc'>Java, Spring Boot, APIs</span></div>"
            f"<div class='welcome-item'><span class='welcome-icon'>🎨</span><span class='welcome-label'>Front-end</span><span class='welcome-desc'>React, componentes, tests</span></div>"
            f"</div>  \n\n"
            "**¿En qué puedo ayudarte hoy?** 😊",
            unsafe_allow_html=True,
        )
