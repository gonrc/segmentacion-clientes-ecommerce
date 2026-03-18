# Segmentacion de Clientes y Analisis Comercial en E-commerce

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

**Trabajo Practico - Ciencia de Datos Aplicada | ITBA | 1er Cuatrimestre 2026 | Grupo 12**

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
- [Make](https://www.gnu.org/software/make/)
- [UV](https://docs.astral.sh/uv/) (gestor de Python, dependencias y entornos virtuales)

### Instalacion

```bash
git clone https://github.com/gonrc/segmentacion-clientes-ecommerce.git
cd segmentacion-clientes-ecommerce

make install_env            # Instala dependencias y configura pre-commit
source .venv/bin/activate   # Activa el entorno virtual
make install_data_libs      # Instala pandas, scikit-learn, jupyter, seaborn
```

### Agregar el dataset

Descargar `Online Retail.xlsx` desde [UCI](https://archive.ics.uci.edu/dataset/352/online+retail) y colocarlo en:

```
data/01_raw/Online Retail.xlsx
```

### Instalar dependencias adicionales

```bash
uv add <paquete>                  # Dependencia del proyecto
uv add --group dev <paquete>      # Dependencia de desarrollo
```

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

| Entrega | Fecha limite | Contenido |
|---------|-------------|-----------|
| **1ra** | 24/03/2026 | Propuesta de proyecto: problema, objetivos, datos, viabilidad |
| **2da** | 28/04/2026 | Recopilacion y preparacion de datos: limpieza, EDA, features |
| **3ra** | 23/06/2026 | Modelado, despliegue y comunicacion de resultados |

## Comandos utiles

```bash
make help                 # Ver todos los comandos disponibles
make test                 # Correr tests con pytest
make check                # Correr linting y formateo
make docs                 # Construir y servir documentacion
```

## Creditos

Proyecto generado a partir del [data science project template](https://github.com/JoseRZapata/data-science-project-template) de [@JoseRZapata](https://github.com/JoseRZapata).
