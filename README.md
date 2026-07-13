# 💻 Santos Pegasus Soluciones — Agente Inteligente RAG

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-red.svg)](https://streamlit.io)
[![Cohere](https://img.shields.io/badge/Cohere-Command_R-yellow.svg)](https://cohere.com)
[![OCI](https://img.shields.io/badge/Deploy-OCI_Compute-orange.svg)](https://oracle.com/cloud)

Asistente técnico impulsado por inteligencia artificial que responde preguntas sobre la documentación interna de **Santos Pegasus Soluciones**, una empresa de tecnología especializada en desarrollo de software escalable bajo arquitectura de microservicios.

Utiliza **RAG (Retrieval-Augmented Generation)** para recuperar información precisa desde **5 documentos PDF técnicos** y generar respuestas en lenguaje natural.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Documentación Cargada](#-documentación-cargada)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Ejecución Local](#-instalación-y-ejecución-local)
- [Ejemplos de Preguntas y Respuestas](#-ejemplos-de-preguntas-y-respuestas)
- [Deploy en OCI](#-deploy-en-oci)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Personalización](#-personalización)
- [Licencia](#-licencia)

---

## 📖 Descripción del Proyecto

**Santos Pegasus Soluciones** es una empresa de tecnología que mantiene una extensa documentación interna: guías de arquitectura, manuales de onboarding, protocolos de incidentes, y estándares de desarrollo front-end y back-end.

Este agente de IA permite a cualquier desarrolladora o desarrollador hacer preguntas en lenguaje natural sobre esa documentación y recibir respuestas inmediatas, sin necesidad de abrir ningún documento. Las conversaciones se **persisten automáticamente** en el navegador: podés cerrar la pestaña, volver a entrar, y la historia sigue ahí.

### ¿Qué problema resuelve?

Los equipos de tecnología pierden horas buscando información en manuales dispersos. Este agente elimina esa fricción: preguntás en lenguaje natural y obtenés la respuesta al instante, con la fuente exacta del documento. Además, las conversaciones se guardan automáticamente: aunque cierres la pestaña, al volver tu historial está intacto.

---

## 📚 Documentación Cargada

El agente tiene acceso a **5 documentos técnicos** (152 páginas en total):

| Documento | Páginas | Contenido Principal |
|---|---|---|
| **🏗️ Arquitectura de Microservicios y Mapa de Dominios** | 31 | Organización de dominios, comunicación entre servicios, patrones de arquitectura |
| **📚 Manual de Onboarding para Nuevos Desarrolladores** | 34 | Proceso de incorporación, herramientas, entorno de desarrollo, convenciones |
| **🚨 Protocolo de Respuesta a Incidentes y Post-Mortems (SRE)** | 38 | Clasificación de incidentes, roles SRE, runbooks, análisis post-mortem |
| **⚙️ Guía Oficial de Ingeniería Back-end** | 12 | Estándares de código, tecnologías back-end, API design, testing |
| **🎨 Guía Oficial de Ingeniería Front-end** | 37 | Frameworks, componentes, diseño responsive, accesibilidad, performance |

---

## 🏗️ Arquitectura

```
                    ┌──────────────────────────────────────────┐
                    │  📁 Docs/Santos Pegasus Soluciones/       │
                    │  ├── Arquitectura de Microservicios.pdf   │
                    │  ├── Manual de Onboarding.pdf             │
                    │  ├── Protocolo de Incidentes.pdf          │
                    │  ├── Guía Back-end.pdf                    │
                    │  └── Guía Front-end.pdf                   │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   DirectoryLoader + PyPDFLoader          │
                    │   (Carga recursiva de todos los PDFs)    │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   RecursiveCharacterTextSplitter         │
                    │   (Chunks de 1000 chars,                 │
                    │    200 de solapamiento)                  │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   Cohere Embeddings                      │
                    │   (embed-multilingual-v3.0)              │
                    │   o HuggingFace (fallback)               │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   Chroma Vector Store                    │
                    │   (Persistente en disco)                 │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   Retriever (top-4 chunks)               │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   Prompt: Sistema + Contexto             │
                    │   "Respondé solo con la info             │
                    │    del contexto..."                      │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   Cohere Command R                       │
                    │   (command-r-08-2024)                    │
                    │   u OpenRouter (fallback)                │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   Streamlit UI                           │
                    │   (Interfaz de chat)                     │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
                    │   ☁️ OCI Compute                        │
                    │   (Deploy en producción)                 │
                    └──────────────────────────────────────────┘
```

### Flujo de datos

```
Pregunta del usuario
       │
       ▼
┌──────────────┐    ┌──────────────────┐    ┌───────────────┐
│  Embeddings  │───▶│  Búsqueda        │───▶│  Contexto     │
│  (pregunta)  │    │  semántica       │    │  (chunks)     │
└──────────────┘    └──────────────────┘    └───────┬───────┘
                                                    │
┌──────────────┐    ┌──────────────────┐            │
│  Respuesta   │◀───│  LLM genera      │◀───────────┘
│  final       │    │  respuesta       │
└──────────────┘    └──────────────────┘
```

---

## 🛠️ Tecnologías

| Tecnología | Versión | Propósito |
|---|---|---|
| **Python** | 3.11+ | Lenguaje principal |
| **LangChain** | 0.3+ | Framework de orquestación RAG |
| **Streamlit** | 1.38+ | Interfaz de usuario web |
| **Cohere** | — | LLM principal (Command R) y embeddings (multilingual v3) |
| **OpenRouter** | — | LLM alternativo (fallback con modelos gratuitos) |
| **HuggingFace** | — | Embeddings alternativos (sentence-transformers) |
| **Chroma** | — | Vector store local persistente |
| **PyPDF** | 5+ | Carga de documentos PDF |
| **OCI Compute** | — | Servidor de producción en la nube |

### ¿Por qué estas tecnologías?

- **LangChain**: Framework más maduro para aplicaciones RAG. Integraciones nativas con Cohere, Chroma y múltiples formatos de documentos.
- **Cohere**: LLM de alta calidad (Command R) + embeddings multilingües. Una sola API key cubre todo el pipeline.
- **Chroma**: Vector store local y persistente. No requiere infraestructura externa.
- **Streamlit**: Interfaz web en pocas líneas. Ideal para prototipos y demos.

---

## 📁 Estructura del Proyecto

```
alura-agente-santos-pegasus/
├── README.md                        # Documentación del proyecto
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Template de variables de entorno
├── .gitignore
├── app.py                           # 🎯 Streamlit app (punto de entrada)
│
├── src/
│   ├── __init__.py
│   ├── config.py                    # Configuración y variables de entorno
│   ├── document_loader.py           # Carga y división de PDFs en chunks
│   ├── vector_store.py              # Embeddings + Chroma vector store
│   └── rag_chain.py                 # Cadena RAG + LLM
│
├── data/
│   ├── chroma_db/                   # Vector store persistente (se genera solo)
│   └── sessions/                    # Sesiones de chat persistentes (se generan al usar)
│
└── scripts/
    └── deploy_oci.sh                # Script de despliegue en OCI

📁 Docs/Santos Pegasus Soluciones/     # PDFs fuente (fuera del repo)
    ├── Arquitectura de Microservicios y Mapa de Dominios.pdf
    ├── Manual de Onboarding para Nuevos Desarrolladores.pdf
    ├── PROTOCOLO DE RESPUESTA A INCIDENTES Y POST-MORTEMS.pdf
    ├── Santo Pegasus Soluciones - Guía Oficial Ingeniería Back-end.pdf
    └── Santo Pegasus Soluciones - Guía Oficial de Ingeniería Front-end.pdf
```

---

## 🚀 Instalación y Ejecución Local

### Requisitos previos

- Python 3.11 o superior
- Los PDFs de Santos Pegasus Soluciones en `../Docs/Santos Pegasus Soluciones/`
- Una cuenta en [Cohere](https://dashboard.cohere.com/) (para la API key gratuita)
- (Opcional) Una cuenta en [OpenRouter](https://openrouter.ai/) para el modo fallback

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/alura-agente-santos-pegasus.git
cd alura-agente-santos-pegasus
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

```bash
cp .env.example .env
```

Editá el archivo `.env` y agregá tu API key de Cohere:

```env
LLM_PROVIDER=cohere
COHERE_API_KEY=tu_api_key_de_cohere
```

> **💡 ¿No tenés API key de Cohere?** Creá una cuenta gratis en [dashboard.cohere.com](https://dashboard.cohere.com/api-keys). El trial incluye 1.000 llamadas/mes.
>
> **💡 ¿Preferís usar OpenRouter?** Cambiá `LLM_PROVIDER=openrouter` y agregá tu key de [openrouter.ai](https://openrouter.ai/settings/keys). El modelo gratuito por defecto es `google/gemma-3n-e2b-it:free`.

### Paso 5: Inicializar el vector store

```bash
python -c "from src.vector_store import build_vector_store; build_vector_store()"
```

Esto va a:
1. Escanear la carpeta `../Docs/Santos Pegasus Soluciones/`
2. Cargar los 5 PDFs (~152 páginas)
3. Partirlos en chunks
4. Generar los embeddings con Cohere
5. Guardarlos en Chroma (`data/chroma_db/`)

### Paso 6: Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501` 🎉

---

## 💬 Ejemplos de Preguntas y Respuestas

### Pregunta 1: Back-end

**Usuario:**
> ¿Qué lenguajes de programación se usan en el back-end?

**Agente:**
> Según la Guía Oficial de Ingeniería Back-end, los lenguajes principales utilizados son **Java 17** y **Kotlin**, con el framework **Spring Boot 3.x** para el desarrollo de microservicios. También se utiliza **Python 3.11+** para tareas de automatización y procesamiento de datos.
>
> *📄 Fuentes: Santo Pegasus Soluciones - Guía Oficial Ingeniería Back-end.pdf (pág. 3)*

---

### Pregunta 2: Onboarding

**Usuario:**
> ¿Cuáles son los pasos del proceso de onboarding para un nuevo desarrollador?

**Agente:**
> El proceso de onboarding consta de 5 fases:
> 1. **Fase 1 - Preparación (Día 0-1):** Configuración del equipo, accesos y herramientas
> 2. **Fase 2 - Entorno Local (Día 2-3):** Instalación y configuración del entorno de desarrollo
> 3. **Fase 3 - Primeros Commits (Día 4-7):** Familiarización con el repositorio y flujo de trabajo Git
> 4. **Fase 4 - Microservicios (Semana 2):** Estudio de la arquitectura y dominios
> 5. **Fase 5 - Asignación (Semana 3):** Incorporación al equipo y primer ticket asignado con mentor
>
> *📄 Fuentes: Manual de Onboarding para Nuevos Desarrolladores - Santo Pegasus Soluciones.pdf (pág. 5)*

---

### Pregunta 3: Incidentes

**Usuario:**
> ¿Qué hago si hay un incidente crítico en producción?

**Agente:**
> Ante un incidente crítico (severidad P0 o P1), seguí estos pasos:
> 1. **Detectar y reportar** en el canal #incidentes de Slack
> 2. **El SRE de turno** asume el rol de Incident Commander
> 3. **Crear un canal dedicado** en Slack para el incidente
> 4. **Evaluar el impacto** y determinar si es necesario escalar
> 5. **Aplicar el runbook** correspondiente al tipo de incidente
> 6. **Comunicar cada 15 minutos** el estado en el canal
> 7. **Resolver o mitigar** el incidente
> 8. **Documentar** la línea de tiempo y acciones tomadas
>
> Después de la resolución, se debe realizar un **Post-Mortem** dentro de las 48 horas hábiles.
>
> *📄 Fuentes: PROTOCOLO DE RESPUESTA A INCIDENTES Y POST-MORTEMS.pdf (pág. 8)*

---

### Pregunta 4: Front-end

**Usuario:**
> ¿Qué framework de front-end recomiendan?

**Agente:**
> La Guía Oficial de Ingeniería Front-end establece que el framework principal es **React 18+** con **TypeScript**. Para nuevos proyectos, se recomienda usar **Next.js 14+** como framework de aplicación. Los componentes se desarrollan siguiendo el patrón **Atomic Design** y se gestionan en la librería interna de componentes.
>
> *📄 Fuentes: Santo Pegasus Soluciones - Guía Oficial de Ingeniería Front-end.pdf (pág. 4)*

---

### Pregunta 5: Fuera de contexto

**Usuario:**
> ¿Cuánto cuesta la cuenta Premium?

**Agente:**
> No tengo información sobre eso en la documentación de Santos Pegasus Soluciones.
>
> *📄 Fuentes: Documentación técnica de Santos Pegasus Soluciones*

---

## 🐳 Deploy Local con Docker

Podés ejecutar el proyecto completo en contenedores Docker como si fuera un despliegue real en producción. El mismo Dockerfile sirve después para subir a OCI sin cambios.

### Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) o Docker Engine (Linux)
- Los PDFs de Santos Pegasus en `../Docs/Santos Pegasus Soluciones/`
- API key de Cohere en un `.env`

### Paso 1: Configurar variables

Asegurate de tener el archivo `.env` con tu API key:

```bash
# Ya debería existir, si no:
cp .env.example .env
# Editá .env y poné tu COHERE_API_KEY
```

### Paso 2: Construir la imagen

```bash
docker compose build
```

Esto crea la imagen con todas las dependencias instaladas. Toma ~2-3 minutos la primera vez.

### Paso 3: Inicializar el vector store (una sola vez)

```bash
docker compose run --rm app-setup
```

Este comando:
1. Carga los 5 PDFs desde `../Docs/Santos Pegasus Soluciones/`
2. Genera los embeddings con Cohere
3. Guarda el vector store en un volumen persistente (`santos-pegasus-chroma`)

> **Nota:** Necesitás conexión a internet para la API de Cohere. El vector store queda persistente entre reinicios del contenedor.

### Paso 4: Iniciar la app

```bash
docker compose up -d
```

La app arranca en segundo plano en `http://localhost:8501`. Podés ver los logs con:

```bash
docker compose logs -f
```

### Administración

| Comando | Qué hace |
|---|---|
| `docker compose up -d` | Iniciar la app en background |
| `docker compose down` | Detener la app |
| `docker compose logs -f` | Ver logs en tiempo real |
| `docker compose build` | Reconstruir la imagen (tras cambios en código) |
| `docker compose run --rm app-setup` | Regenerar vector store (si cambiaron los PDFs) |
| `docker compose exec app rm -rf /app/data/sessions/*` | Limpiar todas las sesiones guardadas |
| `docker compose down -v` | Borrar TODO (incluyendo vector store y sesiones) |

### Estructura de volúmenes

```
Host                          → Contenedor
../Docs/                      → /docs/ (lectura, PDFs fuente)
./data/chroma_db/             → /app/data/chroma_db/ (vector store persistente)
./data/sessions/              → /app/data/sessions/ (sesiones de chat persistentes)
./.env                        → /app/.env (configuración)
```

---

## ☁️ Deploy en OCI

### Requisitos

- Una cuenta en [Oracle Cloud Infrastructure](https://cloud.oracle.com/)
- Una instancia **Compute** (VM.Standard.E2.1.Micro — siempre gratuita)
- Puerto **8501** abierto en el Security List
- Los PDFs de Santos Pegasus Soluciones deben estar accesibles desde la instancia

### Opción 1: Script automático

```bash
# En la instancia OCI
git clone https://github.com/TU_USUARIO/alura-agente-santos-pegasus.git
cd alura-agente-santos-pegasus
bash scripts/deploy_oci.sh
```

> **Importante:** Editá el script `scripts/deploy_oci.sh` y completá la variable `REPO_URL` con la URL de tu repositorio. También asegurate de copiar los PDFs al directorio correcto o ajustar `PDF_DIR` en el `.env`.

### Opción 2: Manual paso a paso

```bash
# 1. Conectarse a la instancia OCI por SSH
ssh -i tu_clave.pem ubuntu@IP_DE_TU_INSTANCIA

# 2. Instalar dependencias
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

# 3. Clonar el proyecto
git clone https://github.com/TU_USUARIO/alura-agente-santos-pegasus.git
cd alura-agente-santos-pegasus

# 4. Copiar los PDFs (ajustá la ruta según corresponda)
# Opción A: Subilos por SCP
# scp -r Docs/Santos\ Pegasus\ Soluciones/ usuario@IP:~/alura-agente-santos-pegasus/../Docs/
# Opción B: Creá la carpeta y ajustá PDF_DIR en .env

# 5. Entorno virtual y dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Configurar .env
cp .env.example .env
nano .env  # Completar COHERE_API_KEY y PDF_DIR si es necesario

# 7. Inicializar vector store
python -c "from src.vector_store import build_vector_store; build_vector_store()"

# 8. Ejecutar Streamlit
screen -S santos-pegasus
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### Abrir puerto en OCI

1. Ir a **Menú → Networking → Virtual Cloud Networks**
2. Seleccionar la VCN de la instancia
3. Ir a **Security Lists** → **Ingress Rules**
4. Agregar regla: `Source: 0.0.0.0/0`, `Destination Port Range: 8501`, `Protocol: TCP`

---

## 📸 Capturas de Pantalla

> **⏳ Espacio reservado para las capturas del deploy.**
>
> Luego del deploy en OCI, agregá acá:
> - Una captura de la aplicación funcionando en la URL pública
> - Un enlace directo a la app desplegada

---

## 🔧 Personalización

### Cambiar los documentos fuente

1. Configurá `PDF_DIR` en `.env` para apuntar a tu propio directorio de PDFs
2. Eliminá la carpeta `data/chroma_db/`
3. Reiniciá la app (el vector store se regenera automáticamente)

### Cambiar de proveedor LLM

Editá `.env`:

```env
# Para usar Cohere (recomendado)
LLM_PROVIDER=cohere
COHERE_API_KEY=tu_key

# Para usar OpenRouter (modelos gratuitos)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=tu_key
OPENROUTER_MODEL=google/gemma-3n-e2b-it:free
```

---

## 📄 Documentación del Proyecto

Este proyecto fue diseñado siguiendo principios de **Clean Architecture** y separación de responsabilidades:

- `src/config.py` — Configuración centralizada (un solo lugar para cambiar rutas, modelos, etc.)
- `src/document_loader.py` — Responsabilidad única: cargar y dividir documentos
- `src/vector_store.py` — Responsabilidad única: gestionar el almacenamiento vectorial
- `src/rag_chain.py` — Responsabilidad única: orquestar la cadena de recuperación y generación
- `app.py` — Solo la capa de presentación (Streamlit)

---

## 📚 Licencia

Este proyecto fue creado como parte del desafío **Alura Agente** — ONE (Oracle Next Education).

---

<p align="center">
  Hecho con ❤️ para el ecosistema ONE<br>
  <strong>Santos Pegasus Soluciones — Ingeniería de clase mundial</strong>
</p>
