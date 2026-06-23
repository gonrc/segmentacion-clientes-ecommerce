# Segmentación de Clientes y Análisis Comercial en E-commerce

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

**Trabajo Práctico - Ciencia de Datos Aplicada | ITBA | 1er Cuatrimestre 2026 | Grupo 12**

> **Estado actual (22/06/2026):** Entregas 01, 02 y 03 finalizadas. Entrega 04 (despliegue + interfaz + presentación oral) en progreso: **API REST (FastAPI)** que expone los modelos, **interfaz Streamlit que consume la API** y orquestación local con **Docker Compose**. Pendiente: despliegue en entorno público y presentación oral.

---

## Descripción del proyecto

Proyecto de analítica comercial sobre el dataset [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) de UCI para segmentar clientes, estimar riesgo de churn y proponer acciones comerciales accionables.

El dataset contiene **541.909 transacciones** de un retailer online del Reino Unido (período: `2010-12-01` a `2011-12-09`). Luego de limpieza se trabaja con **397.884 transacciones válidas**.

## Objetivo de negocio

Construir una solución de datos que permita:

- Segmentar clientes con enfoque RFM + preferencias de producto.
- Detectar clientes con mayor riesgo de churn.
- Priorizar acciones de retención y crecimiento con impacto comercial.

## Resumen por entrega

El Trabajo Práctico se compone de **cuatro entregas**:

| Entrega | Estado | Resultado principal |
|--------|--------|---------------------|
| Entrega 01 - Propuesta de proyecto | Completada | Definición del problema, objetivo de negocio, alcance y elección del dataset. |
| Entrega 02 - Recopilación y preparación de datos | Completada | Adquisición del dataset, EDA, limpieza, RFM y enriquecimiento de productos vía regex. |
| Entrega 03 - Modelado de la solución | Completada | Modelos de segmentación (K-Means) y churn (Random Forest), validación con métricas y persistencia de modelos reutilizables. |
| Entrega 04 - Despliegue y presentación | En progreso | API REST (FastAPI) que expone los modelos + interfaz Streamlit que la consume + Docker Compose. Pendiente: despliegue público y presentación oral. |

Este repositorio refleja la evolución completa del trabajo práctico y queda preparado para iteraciones futuras.

## Entrega 03 - Modelado de la solución (completada)

Foco de la entrega: implementación, validación y persistencia de los modelos. Todo el trabajo es reproducible mediante notebooks.

> **Notebook principal (storytelling para la presentación):** [`notebooks/8-reports/10-gc-entrega03_modelado-2026_06_03.ipynb`](notebooks/8-reports/10-gc-entrega03_modelado-2026_06_03.ipynb). Recorre de punta a punta enfoque, implementación, evaluación, análisis de negocio (segmentos × churn), reflexión crítica y persistencia. Los notebooks de detalle (`07`, `08`, `09`) quedan como respaldo.

### Modelado y validación

- `notebooks/5-models/07-gc-clustering-2026_04_15.ipynb`
  - Clustering de clientes (K-Means) con features RFM + atributos enriquecidos.
  - Preprocesamiento (log1p + estandarización + **PCA**) empaquetado en un `Pipeline` de scikit-learn, serializado junto al modelo para una inferencia reproducible.
  - **Mejora post-feedback (Entrega 03):** se excluyó `Cancel_rate` del clustering (feature ruidosa: 64% de ceros y outliers extremos) y se agregó PCA antes de K-Means. El silhouette subió de **0.17 a 0.31 (+80%)**, con clusters más separados y manteniendo los 4 segmentos de negocio.
- `notebooks/5-models/08-gc-churn-2026_04_16.ipynb`
  - Modelo supervisado de churn (Random Forest) y evaluación con métricas de clasificación (AUC-ROC, F1, precisión, recall, matriz de confusión).
- `notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb`
  - Análisis combinado segmentos + churn, interpretación de negocio y reflexión crítica sobre el rendimiento y posibles mejoras.

### Persistencia de modelos (reutilizables sin reentrenar)

- Modelos: `data/06_models/kmeans_model.pkl`, `data/06_models/churn_model.pkl`
- Salidas: `data/07_model_output/clientes_segmentados.parquet`, `data/07_model_output/churn_predictions.parquet`
- Reporting: `data/08_reporting/*.png` (segmentos, churn y evaluación)

## Entrega 04 - Despliegue y presentación (en progreso)

Foco de la entrega: operacionalizar la solución mediante un servicio e interfaz de uso, y comunicarla en una presentación oral.

### Arquitectura (servicio + interfaz desacoplados)

```
Streamlit (interfaz) ──POST /predict──▶ API REST (FastAPI) ──▶ src/inference (lógica) ──▶ modelos .pkl
```

Separación explícita entre **lógica de modelo** y **capa de servicio**:

- `src/inference/model_service.py` — lógica de inferencia pura (carga de modelos y scoring), sin dependencias de HTTP. Reutilizable por la API, los tests o jobs batch.
- `api/` — capa de servicio FastAPI: validación de entradas/salidas con Pydantic, manejo de errores (422 validación, 503 modelos no cargados, 500 inferencia) y documentación OpenAPI automática en `/docs`.
- `notebooks/7-deploy/streamlit_app.py` — interfaz; el simulador consume la API (`api_client.py`) para scorear clientes nuevos.

Endpoints: `GET /health`, `GET /metadata`, `POST /predict`, `POST /predict/churn`, `POST /predict/segment`, `POST /predict/batch`. Detalle y ejemplos en [`deploy/README.md`](deploy/README.md).

### Levantar la solución (Docker)

```bash
docker compose -f deploy/docker-compose.yml up --build
# API:       http://localhost:8000/docs
# Interfaz:  http://localhost:8501
```

Vista del prototipo:

![Prototipo Streamlit - simulador de churn y segmento](assets/streamlit-simulador-entrega04.png)

### Tests

```bash
uv run pytest tests/test_api.py tests/inference/test_model_service.py -v
```

### Pendiente

- Despliegue en un entorno público accesible (p. ej. Render/Railway para la API + Streamlit Cloud).
- Presentación oral del proyecto (10-15 min) con demostración en vivo.

---

## Dataset y enriquecimiento

| Atributo | Detalle |
|----------|---------|
| Fuente | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail) |
| Archivo | `Online Retail.xlsx` |
| Registros | 541.909 originales -> 397.884 válidos |
| Clientes únicos | 4.338 |
| Variables originales | `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country` |
| Enriquecimiento | +50 atributos por producto derivados de `Description` (regex) |

Descarga directa del dataset: [online+retail.zip](https://archive.ics.uci.edu/static/public/352/online+retail.zip)

---

## Configuración del entorno

### Requisitos

- Python `>=3.11`
- Git
- (opcional) Make

### Instalación rápida

```bash
git clone https://github.com/gonrc/segmentacion-clientes-ecommerce.git
cd segmentacion-clientes-ecommerce

# Opción recomendada (uv): crea el entorno e instala runtime + dev + docs
uv sync

# Si no tenés uv instalado:
pip install uv && uv sync
```

Esto crea el entorno virtual en `.venv/` con todas las dependencias necesarias (incluido Streamlit para el prototipo).

### Cargar dataset crudo

```bash
curl -L -o data/01_raw/online_retail.zip https://archive.ics.uci.edu/static/public/352/online+retail.zip
unzip data/01_raw/online_retail.zip -d data/01_raw/
```

---

## Ejecución reproducible (pipeline Entrega 03)

Para regenerar artefactos de modelado y reportes:

```bash
.venv/bin/python execute_notebook.py "notebooks/4-feat_eng/06-gc-customer_product_profile-2026_04_01.ipynb"
.venv/bin/python execute_notebook.py "notebooks/5-models/07-gc-clustering-2026_04_15.ipynb"
.venv/bin/python execute_notebook.py "notebooks/5-models/08-gc-churn-2026_04_16.ipynb"
.venv/bin/python execute_notebook.py "notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb"
```

Si ya existen artefactos previos en `data/`, se recomienda regenerarlos con esta secuencia para asegurar consistencia de resultados.

---

## Ejecutar la app Streamlit

```bash
.venv/bin/streamlit run "notebooks/7-deploy/streamlit_app.py" --server.fileWatcherType none
```

Por defecto queda disponible en `http://127.0.0.1:8501`.

---

## Estructura del proyecto

```text
.
├── api/                # Capa de servicio (FastAPI): main.py, schemas.py
├── deploy/             # Dockerfile, docker-compose.yml y guía de despliegue
├── conf/
├── data/
│   ├── 01_raw/
│   ├── 02_intermediate/
│   ├── 03_primary/
│   ├── 04_feature/
│   ├── 05_model_input/
│   ├── 06_models/
│   ├── 07_model_output/
│   └── 08_reporting/
├── notebooks/
│   ├── 1-data/
│   ├── 2-exploration/
│   ├── 3-analysis/
│   ├── 4-feat_eng/
│   ├── 5-models/
│   ├── 6-interpretation/
│   ├── 7-deploy/       # streamlit_app.py + api_client.py
│   └── 8-reports/
├── src/
│   └── inference/      # model_service.py (lógica de modelo)
├── tests/
├── pyproject.toml
└── README.md
```

## Qué revisar primero (docentes)

Para una revisión rápida de los entregables:

1. `README.md` (este documento).
2. Entrega 03 (modelado):
   - **Principal:** `notebooks/8-reports/10-gc-entrega03_modelado-2026_06_03.ipynb` (notebook unificado de presentación).
   - Detalle: `notebooks/5-models/07-gc-clustering-2026_04_15.ipynb`.
   - Detalle: `notebooks/5-models/08-gc-churn-2026_04_16.ipynb`.
   - Detalle: `notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb`.
3. Entrega 04 (despliegue e interfaz):
   - `deploy/README.md` (arquitectura y cómo levantar la solución).
   - `api/main.py` (capa de servicio) + `src/inference/model_service.py` (lógica de modelo).
   - `notebooks/7-deploy/streamlit_app.py` (interfaz que consume la API).

## Nota sobre versionado de datos

Los archivos de `data/` están excluidos del repositorio por tamaño.  
Para correr notebooks/app en otra máquina, hay que descargar el dataset y regenerar los artefactos locales.

## Créditos

Proyecto basado en el [data science project template](https://github.com/JoseRZapata/data-science-project-template).
