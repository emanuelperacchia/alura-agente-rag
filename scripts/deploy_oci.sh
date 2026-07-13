#!/bin/bash
# ============================================================
# Santos Pegasus Soluciones - Deploy en OCI Compute
# ============================================================
# Uso:
#   1. Crear una instancia en OCI Compute (Ubuntu 22.04+)
#   2. Subir este script y el proyecto a la instancia
#   3. Ejecutar: bash scripts/deploy_oci.sh
#
# Requisitos:
#   - Git, Python 3.11+, pip
#   - Puerto 8501 abierto en el Security List de OCI
#   - Los PDFs de Santos Pegasus en el directorio correcto
# ============================================================

set -e

echo "========================================"
echo "  Santos Pegasus Soluciones - Deploy"
echo "========================================"

# ─── Configuración ──────────────────────────────────────────
PROJECT_DIR="$HOME/santos-pegasus-rag"
REPO_URL="https://github.com/emanuelperacchia/alura-agente-rag.git"
STREAMLIT_PORT=8501
PDF_DIR="$PROJECT_DIR/../Docs/Santos Pegasus Soluciones"

# ─── 1. Instalar dependencias del sistema ──────────────────
echo "[1/6] Instalando dependencias del sistema..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git curl

# ─── 2. Clonar repositorio ────────────────────────────────
echo "[2/6] Clonando repositorio..."
if [ -d "$PROJECT_DIR" ]; then
    echo "Directorio existe. Actualizando..."
    cd "$PROJECT_DIR" && git pull
else
    if [ -n "$REPO_URL" ]; then
        git clone "$REPO_URL" "$PROJECT_DIR"
    else
        echo "⚠️  No se configuró REPO_URL."
        echo "   Subí los archivos manualmente a $PROJECT_DIR"
        mkdir -p "$PROJECT_DIR"
    fi
fi

cd "$PROJECT_DIR"

# ─── 3. Crear entorno virtual e instalar dependencias ──────
echo "[3/6] Instalando dependencias Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ─── 4. Configurar variables de entorno ────────────────────
echo "[4/6] Configurando variables de entorno..."
if [ ! -f .env ]; then
    echo "⚠️  No se encontró .env. Creando desde .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 EDITÁ EL ARCHIVO .env CON TUS API KEYS:"
    echo "   nano $PROJECT_DIR/.env"
    echo ""
    read -p "   Presioná Enter después de editar el archivo..."
fi

# ─── 5. Crear directorios de datos e inicializar vector store ──
echo "[5/6] Creando directorios de datos e inicializando vector store..."
mkdir -p data/chroma_db data/sessions
source venv/bin/activate
python -c "from src.vector_store import build_vector_store; build_vector_store()"

# ─── 6. Iniciar Streamlit ─────────────────────────────────
echo "[6/6] Iniciando Streamlit en puerto $STREAMLIT_PORT..."
echo ""
echo "========================================"
echo "  ✅ Santos Pegasus desplegado correctamente"
echo "  📍 http://$(curl -s ifconfig.me):$STREAMLIT_PORT"
echo "  💡 Para mantenerlo corriendo después"
echo "     de cerrar la terminal, usá:"
echo "     screen -S santos-pegasus"
echo "     y ejecutá este script nuevamente"
echo "========================================"

source venv/bin/activate
streamlit run app.py \
    --server.port=$STREAMLIT_PORT \
    --server.address=0.0.0.0 \
    --server.enableCORS=false
