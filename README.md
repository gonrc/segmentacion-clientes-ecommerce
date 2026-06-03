# Segmentacion de Clientes y Analisis Comercial en E-commerce

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

**Trabajo Practico - Ciencia de Datos Aplicada | ITBA | 1er Cuatrimestre 2026 | Grupo 12**

> **Estado actual (03/06/2026):** Entregas 01 y 02 finalizadas. Entrega 03 implementada en `main` con notebooks reproducibles de modelado (`07`, `08`, `09`) y prototipo funcional en Streamlit.

---

## Descripcion del proyecto

Proyecto de analitica comercial sobre el dataset [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) de UCI para segmentar clientes, estimar riesgo de churn y proponer acciones comerciales accionables.

El dataset contiene **541.909 transacciones** de un retailer online del Reino Unido (periodo: `2010-12-01` a `2011-12-09`). Luego de limpieza se trabaja con **397.884 transacciones validas**.

## Objetivo de negocio

Construir una solucion de datos que permita:

- Segmentar clientes con enfoque RFM + preferencias de producto.
- Detectar clientes con mayor riesgo de churn.
- Priorizar acciones de retencion y crecimiento con impacto comercial.

## Resumen por entrega

| Entrega | Estado | Resultado principal |
|--------|--------|---------------------|
| Entrega 01 | Completada | Definicion del problema, alcance y dataset base. |
| Entrega 02 | Completada | Limpieza, EDA, RFM y enriquecimiento de productos via regex. |
| Entrega 03 | Completada (implementacion) | Modelos de segmentacion + churn, validacion e interfaz funcional en Streamlit. |

Este repositorio refleja la evolucion completa del trabajo practico y queda preparado para iteraciones futuras.

## Alcance Entrega 03 (actual)

### Modelado y validacion

- `notebooks/5-models/07-gc-clustering-2026_04_15.ipynb`
  - Clustering de clientes (K-Means) con features RFM + atributos enriquecidos.
- `notebooks/5-models/08-gc-churn-2026_04_16.ipynb`
  - Modelo supervisado de churn y evaluacion con metricas de clasificacion.
- `notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb`
  - Analisis combinado segmentos + churn, interpretacion y reflexion critica.

### Prototipo funcional

- `notebooks/7-deploy/streamlit_app.py`
  - Exploracion de segmentos.
  - Ranking de clientes en riesgo.
  - Buscador de cliente.
  - Simulador de nuevos clientes con muestreo aleatorio realista.
  - Seccion de propuesta de despliegue.

Vista del prototipo:

![Prototipo Streamlit - simulador de churn y segmento](assets/streamlit-simulador-entrega03.png)

### Artefactos esperados

- Modelos: `data/06_models/kmeans_model.pkl`, `data/06_models/churn_model.pkl`
- Salidas: `data/07_model_output/clientes_segmentados.parquet`, `data/07_model_output/churn_predictions.parquet`
- Reporting: `data/08_reporting/*.png` (segmentos, churn y evaluacion)

---

## Dataset y enriquecimiento

| Atributo | Detalle |
|----------|---------|
| Fuente | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail) |
| Archivo | `Online Retail.xlsx` |
| Registros | 541.909 originales -> 397.884 validos |
| Clientes unicos | 4.338 |
| Variables originales | `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country` |
| Enriquecimiento | +50 atributos por producto derivados de `Description` (regex) |

Descarga directa del dataset: [online+retail.zip](https://archive.ics.uci.edu/static/public/352/online+retail.zip)

---

## Configuracion del entorno

### Requisitos

- Python `>=3.11`
- Git
- (opcional) Make

### Instalacion rapida

Las dependencias se declaran en un unico lugar: **`pyproject.toml`** (con versiones exactas fijadas en `uv.lock`). No hay listas de paquetes duplicadas en este README ni un `requirements.txt` paralelo, para evitar divergencias.

```bash
git clone https://github.com/gonrc/segmentacion-clientes-ecommerce.git
cd segmentacion-clientes-ecommerce

# Opcion recomendada (uv): crea el entorno e instala runtime + dev + docs
uv sync

# Si no tenes uv instalado:
pip install uv && uv sync
```

Esto crea el entorno virtual en `.venv/` con todas las dependencias necesarias (incluido Streamlit para el prototipo).

### Cargar dataset crudo

```bash
curl -L -o data/01_raw/online_retail.zip https://archive.ics.uci.edu/static/public/352/online+retail.zip
unzip data/01_raw/online_retail.zip -d data/01_raw/
```

---

## Ejecucion reproducible (pipeline Entrega 03)

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
│   ├── 7-deploy/
│   └── 8-reports/
├── src/
├── tests/
├── pyproject.toml
└── README.md
```

## Que revisar primero (docentes)

Para una revision rapida del entregable:

1. `README.md` (este documento).
2. `notebooks/5-models/07-gc-clustering-2026_04_15.ipynb`.
3. `notebooks/5-models/08-gc-churn-2026_04_16.ipynb`.
4. `notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb`.
5. `notebooks/7-deploy/streamlit_app.py` (prototipo).

## Nota sobre versionado de datos

Los archivos de `data/` estan excluidos del repositorio por tamano.  
Para correr notebooks/app en otra maquina, hay que descargar el dataset y regenerar los artefactos locales.

## Creditos

Proyecto basado en el [data science project template](https://github.com/JoseRZapata/data-science-project-template).
