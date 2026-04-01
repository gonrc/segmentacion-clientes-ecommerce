# Segmentacion de Clientes y Analisis Comercial en E-commerce

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

**Trabajo Practico - Ciencia de Datos Aplicada | ITBA | 1er Cuatrimestre 2026 | Grupo 12**

> **Estado actual (01/04/2026):** ✅ Entrega 02 completada | 🔄 Enriquecimiento de datos en progreso | ⏳ Entrega 03 pendiente

---

## Descripcion del proyecto

Proyecto de analitica comercial que utiliza datos transaccionales del dataset [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) de UCI para generar conocimiento accionable sobre el comportamiento de clientes y ventas en un e-commerce.

El dataset contiene **541.909 transacciones** de un retailer online del Reino Unido (periodo: 01/12/2010 - 09/12/2011). La empresa vende regalos y articulos varios, y gran parte de sus clientes son mayoristas.

## Problema de negocio

La empresa cuenta con datos de transacciones pero no dispone de una vision clara de:

- Que segmentos de clientes tiene
- Cuales generan mas ingreso
- Que patrones de compra se repiten
- Que senales anticipan cancelaciones o menor valor comercial

## Objetivos

**Objetivo principal:** Generar conocimiento accionable sobre el comportamiento de clientes y ventas para mejorar la segmentacion comercial y la toma de decisiones.

**Subobjetivos:**

- Identificar segmentos de clientes segun frecuencia, recencia y gasto (RFM)
- Detectar que productos o categorias concentran mayor facturacion
- Analizar la distribucion geografica de ventas por pais
- Estudiar patrones de cancelacion de transacciones
- Construir una base analitica para futuros modelos predictivos o dashboards

## Dataset

| Atributo | Detalle |
|----------|---------|
| **Fuente** | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail) |
| **Archivo** | `Online Retail.xlsx` |
| **Registros** | 541.909 transacciones |
| **Periodo** | 01/12/2010 - 09/12/2011 |
| **Variables** | InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country |

Descarga directa: [online+retail.zip](https://archive.ics.uci.edu/static/public/352/online+retail.zip)

## Configuracion del entorno

### Requisitos previos

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) >= 3.11
- [Make](https://www.gnu.org/software/make/) (opcional)

### Instalacion

```bash
git clone https://github.com/gonrc/segmentacion-clientes-ecommerce.git
cd segmentacion-clientes-ecommerce

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install pandas openpyxl pyarrow matplotlib seaborn jupyter nbconvert scikit-learn
```

### Agregar el dataset

Descargar y descomprimir `Online Retail.xlsx`:

```bash
curl -L -o data/01_raw/online_retail.zip https://archive.ics.uci.edu/static/public/352/online+retail.zip
unzip data/01_raw/online_retail.zip -d data/01_raw/
```

O descargar manualmente desde [UCI](https://archive.ics.uci.edu/dataset/352/online+retail) y colocar en `data/01_raw/Online Retail.xlsx`

## Estructura del proyecto

```
.
├── conf/                          # Archivos de configuracion
├── data/
│   ├── 01_raw/                    # Datos crudos (Online Retail.xlsx)
│   ├── 02_intermediate/           # Datos con tipos corregidos
│   ├── 03_primary/                # Datos limpios y transformados
│   ├── 04_feature/                # Features (ej: tabla RFM por cliente)
│   ├── 05_model_input/            # Tablas listas para modelado
│   ├── 06_models/                 # Modelos serializados
│   ├── 07_model_output/           # Resultados de modelos
│   └── 08_reporting/              # Datos para reportes y dashboards
├── notebooks/
│   ├── 1-data/                    # Carga, limpieza y preparacion
│   ├── 2-exploration/             # Analisis exploratorio (EDA)
│   ├── 3-analysis/                # Analisis estadistico
│   ├── 4-feat_eng/                # Ingenieria de features (RFM, etc.)
│   ├── 5-models/                  # Entrenamiento (clustering, etc.)
│   ├── 6-interpretation/          # Interpretacion de segmentos
│   ├── 7-deploy/                  # Despliegue
│   └── 8-reports/                 # Narrativa y conclusiones
├── src/                           # Codigo fuente reutilizable
│   ├── data/                      # Funciones de extraccion y procesamiento
│   ├── model/                     # Funciones de entrenamiento y evaluacion
│   ├── inference/                 # Prediccion y serving
│   └── pipelines/                 # Pipelines (feature, training, inference)
├── tests/                         # Tests del proyecto
├── Makefile                       # Comandos de automatizacion
├── pyproject.toml                 # Dependencias y configuracion
└── README.md
```

## Roadmap del proyecto

| Entrega | Fecha limite | Estado | Contenido |
|---------|-------------|--------|-----------|
| **1ra** | 24/03/2026 | ✅ Completada (25/03/2026) | Propuesta de proyecto: problema, objetivos, datos, viabilidad |
| **2da** | 28/04/2026 | ✅ Completada (24/03/2026) | Recopilacion y preparacion de datos: limpieza, EDA, features RFM |
| **Post-feedback** | - | 🔄 En progreso | Enriquecimiento de dataset con extraccion de atributos (colores, materiales, estilos) |
| **3ra** | 23/06/2026 | ⏳ Pendiente | Clustering, segmentacion avanzada, prototipo y presentacion |

### Notebooks entregados

**Entrega 02 (24/03/2026):**
- `01-gc-carga_y_limpieza-2026_03_18.ipynb` - Carga, limpieza y justificacion del dataset
- `02-gc-eda_ventas-2026_03_18.ipynb` - Analisis exploratorio con 10 visualizaciones
- `04-gc-rfm_por_cliente-2026_03_18.ipynb` - Feature engineering RFM y reflexion final

**Trabajo adicional (01/04/2026):**
- `05-gc-product_enrichment_regex-2026_04_01.ipynb` - Extraccion de atributos con regex
- `06-gc-customer_product_profile-2026_04_01.ipynb` - Perfiles de cliente por preferencias de producto

## Notebooks y analisis

### Ejecutar notebooks

```bash
jupyter notebook  # Abrir interfaz de Jupyter
```

Los notebooks estan organizados por fase en `notebooks/`:
- `1-data/` - Carga y limpieza
- `2-exploration/` - Analisis exploratorio
- `4-feat_eng/` - Ingenieria de features (RFM, atributos de producto)
- `5-models/` - Clustering y segmentacion (proximo)

### Verificacion de cumplimiento

Ver `notebooks/ENTREGA02_CUMPLIMIENTO.md` para detalles de cumplimiento de requisitos de la Entrega 02.

## Creditos

Proyecto generado a partir del [data science project template](https://github.com/JoseRZapata/data-science-project-template) de [@JoseRZapata](https://github.com/JoseRZapata).
