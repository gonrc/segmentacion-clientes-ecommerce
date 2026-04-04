# CLAUDE.md - Proyecto: Segmentación de Clientes E-commerce

## Contexto del Proyecto

**Materia:** Ciencia de Datos Aplicada - ITBA - 1er Cuatrimestre 2026
**Grupo:** Grupo 12
**Repositorio:** `segmentacion-clientes-ecommerce/`

### Problema de Negocio
Análisis de comportamiento de clientes y ventas en e-commerce usando el dataset "Online Retail" de UCI (541,909 transacciones, período 01/12/2010 - 09/12/2011). La empresa necesita segmentación de clientes, identificación de patrones de compra y análisis predictivo.

### Objetivos
- Identificar segmentos de clientes según RFM (Recency, Frequency, Monetary)
- Detectar productos/categorías con mayor facturación
- Analizar distribución geográfica de ventas
- Estudiar patrones de cancelación de transacciones
- Construir base analítica para modelos predictivos y dashboards

### Hallazgos Clave (Entrega 02)
**Datos:**
- 541,909 transacciones originales → 397,884 válidas después de limpieza
- 4,338 clientes únicos, 3,877 productos, 37 países
- 24.9% de registros sin CustomerID (eliminados)
- 8,905 cancelaciones separadas (~$601k de valor cancelado)

**Concentración:**
- UK representa 82% del revenue total (distribución geográfica muy sesgada)
- Patrón Pareto confirmado: top 20% de clientes genera la mayoría del revenue
- Pocos productos concentran facturación significativa

**Temporalidad:**
- Pico de ventas septiembre-noviembre (compras navideñas)
- No hay ventas los sábados
- Horas pico: 10-15hs

**Calidad de Datos:**
- 1,556 clientes (35.9%) tienen al menos una cancelación
- 13 clientes con revenue neto negativo (cancelaron más de lo que compraron)
- Correlación alta entre Frequency y Monetary (~0.7)
- Cancel_rate aporta información nueva (baja correlación con RFM)

**Enriquecimiento de Productos (Post-Feedback Entrega 01):**
- 3,877 productos únicos enriquecidos con regex (01/04/2026)
- 34.20% tienen color extraído, 15.73% material, 8.38% tamaño, 13.54% estilo
- 59.68% de productos tienen al menos 1 atributo detectado
- 40.21% requieren inferencia semántica con LLM (Fase 2, pendiente)
- +50 atributos nuevos por producto (flags binarios + listas + métricas)

## Entregas del Trabajo Práctico

### Entrega 01 - Propuesta de Proyecto (24/03/2026)
**Estado:** ✅ COMPLETADA
**Ubicación:** `[01] Propuesta de proyecto - Grupo 12 - Ecommerce.pdf`
**Presentación:** 25/03/2026

**Feedback recibido (25/03/2026):**
Los profesores señalaron que el dataset tiene pocas variables (solo 8 columnas), lo cual limita el análisis. Sugirieron enriquecer el dataset usando el campo `Description` del producto para:
- Extraer atributos adicionales (categorías, materiales, colores, tamaños)
- Usar técnicas de NLP/LLM para categorización semántica
- Generar análisis más profundo sobre comportamiento de compra por tipo de producto

**Acción tomada:**
✅ **COMPLETADA (01/04/2026):** Implementación de enriquecimiento con regex (Fase 1). Ver sección "Enriquecimiento del Campo Description" para detalles.

### Entrega 02 - Recopilación y Preparación de Datos (28/04/2026)
**Estado:** ✅ COMPLETADA (actualizada 03/04/2026 con enriquecimiento)
**Commit inicial:** `b0264f6` - "Entrega 02: Agregar justificación del dataset y reflexión final completa"
**Commit enriquecimiento:** `b372c48` - "Feat: Enriquecimiento de dataset con regex y perfiles de cliente"
**Formato:** Enlace a repositorio GitHub
**Presentación:** 29/04/2026

**Notebooks entregados:**
- `notebooks/1-data/01-gc-carga_y_limpieza-2026_03_18.ipynb` - Con justificación del dataset
- `notebooks/2-exploration/02-gc-eda_ventas-2026_03_18.ipynb` - EDA completo con 14 visualizaciones (10 originales + 4 de enriquecimiento)
- `notebooks/4-feat_eng/04-gc-rfm_por_cliente-2026_03_18.ipynb` - RFM + Reflexión final completa
- `notebooks/4-feat_eng/05-gc-product_enrichment_regex-2026_04_01.ipynb` - Enriquecimiento con regex + visualizaciones

**Contenido completado:**
- ✅ Adquisición del dataset Online Retail.xlsx (23 MB descargado)
- ✅ Justificación formal de elección del dataset (6 razones)
- ✅ Análisis exploratorio (14 gráficos PNG generados)
- ✅ Limpieza y transformación (397,884 registros válidos)
- ✅ Diagnóstico de calidad (CustomerID nulos 24.9%, cancelaciones, outliers)
- ✅ Feature engineering RFM con Monetary neteado
- ✅ **Enriquecimiento de productos con regex (+50 atributos por producto)**
- ✅ Reflexión final (decisiones, dificultades, siguientes pasos)
- ✅ Preparación para modelado (tabla RFM de 4,338 clientes + productos enriquecidos)

**Archivos generados:**
- `data/01_raw/Online Retail.xlsx` (23 MB)
- `data/03_primary/ventas_limpias.parquet` (3.0 MB, 397,884 registros)
- `data/03_primary/cancelaciones.parquet` (163 KB, 8,905 registros)
- `data/04_feature/rfm_clientes.parquet` (73 KB, 4,338 clientes)
- `data/04_feature/rfm_clientes_detalle.parquet` (113 KB)
- `data/04_feature/productos_enriquecidos_regex.parquet` (108 KB, 3,877 productos con 58 columnas)
- `data/04_feature/rfm_clientes_enriched.parquet` (160 KB, con preferencias de producto)
- `data/08_reporting/*.png` (14 visualizaciones: 10 EDA + 4 enriquecimiento)

**Verificación:** Ver `notebooks/ENTREGA02_CUMPLIMIENTO.md` para cumplimiento 100% con PDF de consigna

### Entrega 03 - Modelado y Presentación (23/06/2026)
**Contenido esperado:**
- Implementación de modelos (predictivos/descriptivos/clustering)
- Validación con métricas apropiadas
- Prototipo funcional (Streamlit/Flask/Dashboard)
- Propuesta de despliegue
- Presentación oral (10-15 min)

## Estructura del Repositorio

```
segmentacion-clientes-ecommerce/
├── conf/                       # Configuraciones por módulo
│   ├── config.yml
│   ├── data_extraction/
│   ├── data_preparation/
│   ├── data_validation/
│   ├── model_train/
│   ├── model_evaluation/
│   ├── model_validation/
│   └── model_serving/
├── data/                       # Pipeline de datos
│   ├── 01_raw/                 # Online Retail.xlsx
│   ├── 02_intermediate/        # Tipos corregidos
│   ├── 03_primary/             # Datos limpios
│   ├── 04_feature/             # Features (RFM, etc.)
│   ├── 05_model_input/         # Listas para modelado
│   ├── 06_models/              # Modelos serializados
│   ├── 07_model_output/        # Resultados de modelos
│   └── 08_reporting/           # Datos para reportes
├── notebooks/                  # Notebooks organizados por fase
│   ├── 1-data/                 # Carga y limpieza
│   ├── 2-exploration/          # EDA
│   ├── 3-analysis/             # Análisis estadístico
│   ├── 4-feat_eng/             # Ingeniería de features
│   ├── 5-models/               # Entrenamiento
│   ├── 6-interpretation/       # Interpretación
│   ├── 7-deploy/               # Despliegue
│   └── 8-reports/              # Narrativa final
├── src/                        # Código fuente reutilizable
│   ├── data/
│   ├── model/
│   ├── inference/
│   └── pipelines/
└── tests/                      # Tests del proyecto
```

## Dataset

**Fuente:** [UCI Machine Learning Repository - Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)
**Archivo:** `Online Retail.xlsx`
**Ubicación:** `data/01_raw/Online Retail.xlsx`

**Variables originales:**
- InvoiceNo: Número de factura
- StockCode: Código de producto
- Description: Descripción del producto ⚡ *Campo a enriquecir con NLP/LLM*
- Quantity: Cantidad vendida
- InvoiceDate: Fecha de transacción
- UnitPrice: Precio unitario
- CustomerID: ID del cliente
- Country: País del cliente

**Variables derivadas planificadas (post-enriquecimiento):**
- Color, Material, Tamaño, Estilo (extracción regex)
- Categoría (3 niveles), Función, Ocasión, Forma (inferencia LLM)
- Complejidad, PrecioUnitarioReal, DensidadInfo, Seasonal_flag (calculados)

**Características:**
- 541,909 transacciones
- Período: 01/12/2010 - 09/12/2011
- Retailer online del Reino Unido
- Mayoristas como principales clientes

## Stack Tecnológico

### Gestión de Entorno
- **UV:** Gestor de Python y dependencias (reemplaza pip/poetry/pyenv) - ⚠️ NO instalado en el sistema actual
- **Python:** >= 3.11 (3.11.9 via pyenv)
- **venv:** Entorno virtual Python estándar (usado como alternativa a UV)
- **Make:** Automatización de tareas (disponible)

### Librerías Core
- **pandas[parquet]** >= 3.0.1
- **numpy** >= 2.4.3
- **scipy** >= 1.17.1
- **scikit-learn** >= 1.8.0
- **openpyxl** >= 3.1.5

### Desarrollo
- **jupyter** >= 1.1.1
- **matplotlib** >= 3.10.8
- **seaborn** >= 0.13.2
- **pytest** >= 9.0.2
- **pre-commit** >= 4.5.1

### Documentación
- **mkdocs** >= 1.6.1
- **mkdocs-material** >= 9.7.5

## Comandos Importantes

### Configuración Inicial

**Con UV (si está instalado):**
```bash
cd segmentacion-clientes-ecommerce
make install_env              # Instala deps y pre-commit
source .venv/bin/activate     # Activa entorno virtual
make install_data_libs        # Instala librerías de data science
```

**Con venv manual (usado actualmente):**
```bash
cd segmentacion-clientes-ecommerce
python3 -m venv .venv
source .venv/bin/activate
pip install pandas openpyxl pyarrow matplotlib seaborn jupyter nbconvert
```

### Instalación de Dependencias

**Con UV:**
```bash
uv add <paquete>                    # Dependencia del proyecto
uv add --group dev <paquete>        # Dependencia de desarrollo
```

**Con pip (alternativa actual):**
```bash
pip install <paquete>               # Cualquier paquete
```

### Testing y Calidad
```bash
make test                     # Ejecuta tests con pytest + coverage
make test_verbose             # Tests en modo verbose
make check                    # Linting y formateo (pre-commit)
make lint                     # Solo ruff
```

### Documentación
```bash
make docs                     # Construir y servir docs (mkdocs)
make docs_test                # Test de compilación de docs
```

### Git
```bash
make switch_main              # Cambia a main y pull
make clean_branchs            # Limpia branches mergeadas
```

### Limpieza
```bash
make clean_env                # Elimina .venv
```

## Convenciones de Notebooks

**Nomenclatura:** `NN-<iniciales>-<tema>-YYYY_MM_DD.ipynb`

Ejemplo: `01-gc-carga_y_limpieza-2026_03_18.ipynb`

**Ubicación según fase:**
- `1-data/`: Carga, limpieza, preparación
- `2-exploration/`: EDA y visualizaciones
- `3-analysis/`: Análisis estadístico
- `4-feat_eng/`: RFM, features derivadas
- `5-models/`: Clustering, clasificación, regresión
- `6-interpretation/`: Análisis de segmentos
- `7-deploy/`: Prototipos (Streamlit/Flask)
- `8-reports/`: Narrativa y conclusiones

## Workflow del Proyecto

### Fase 1: Preparación (Entrega 02)
1. Descargar dataset en `data/01_raw/`
2. Notebook de carga y limpieza (`1-data/`)
3. Notebook de EDA (`2-exploration/`)
4. Transformaciones y features (`4-feat_eng/`)
5. Documentar decisiones y dificultades

### Fase 2: Modelado (Entrega 03)
1. Ingeniería de features (RFM, segmentación)
2. Entrenamiento de modelos (`5-models/`)
   - Clustering (K-Means, DBSCAN)
   - Clasificación (Random Forest, LightGBM)
   - Regresión (XGBoost)
3. Evaluación con métricas apropiadas
4. Interpretación de resultados (`6-interpretation/`)

### Fase 3: Despliegue y Comunicación
1. Prototipo funcional (`7-deploy/`)
   - Streamlit app para segmentación
   - Dashboard interactivo
   - API Flask para predicciones
2. Propuesta de despliegue (MLOps, cloud)
3. Documentación final (`8-reports/`)
4. Presentación oral (10-15 min)

## Metodología de Trabajo

### Modelo de Proceso
Basado en **CRISP-DM** (Cross-Industry Standard Process for Data Mining):
1. Comprensión del negocio
2. Comprensión de los datos
3. Preparación de los datos
4. Modelado
5. Evaluación
6. Despliegue

### Control de Calidad
- **Pre-commit hooks:** Linting automático (ruff)
- **Testing:** pytest con cobertura mínima
- **Type checking:** mypy configurado
- **Documentación:** Código documentado en notebooks

## Técnicas de Machine Learning

### Aprendizaje No Supervisado
- **Clustering K-Means:** Segmentación de clientes
- **t-SNE/UMAP:** Visualización de segmentos

### Aprendizaje Supervisado
- **Random Forest / LightGBM:** Clasificación (churn, categorización)
- **XGBoost:** Regresión (predicción de ventas, CLV)

### Feature Engineering
- **RFM Analysis:** Recency, Frequency, Monetary value
- **Product Attributes:** Color, Material, Tamaño, Estilo/Tema, Categoría jerárquica (3 niveles)
- **Product Behavior:** Función (decorative/functional/gift), Ocasión (Christmas/party/kids), Forma
- **Derived Features:** Lifetime value, Cancel_rate, Seasonal_flag, Complejidad (single/set), PrecioUnitarioReal

## Consideraciones Especiales

### Datos Faltantes
- CustomerID tiene valores nulos significativos (24.9%)
- **Decisión aplicada:** Eliminar registros sin CustomerID (imposible atribuirlos a un cliente para segmentación)

### Outliers
- UnitPrice y Quantity pueden tener valores extremos (ej: Quantity=80,995)
- Devoluciones (Quantity negativa)
- **Decisión aplicada:** Documentar pero NO eliminar automáticamente. Clipping al P99 solo para visualizaciones.
- **Razón:** Outliers legítimos (clientes VIP con compras grandes) son relevantes para segmentación

### Cancelaciones
- InvoiceNo que comienzan con "C" son cancelaciones (8,905 registros)
- **Decisión aplicada:** Separar en dataset independiente y netear contra revenue bruto
- **Resultado:** Monetary neto por cliente, Cancel_rate como feature adicional

### Geografía
- Mayoría de ventas en UK (82%)
- **Decisión aplicada:** Trabajar con todos los países juntos, documentar el sesgo
- **Consideración futura:** Segmentación estratificada por región si patrones UK no son representativos

## Enriquecimiento del Campo Description

### Contexto y Justificación
Tras el feedback de los profesores (25/03/2026) sobre la limitación de variables del dataset, se identificó que el campo `Description` contiene información latente no estructurada que puede extraerse para enriquecer el análisis.

### Hallazgos de la Exploración (25/03/2026)

**Estadísticas Generales:**
- 397,884 registros × 3,877 productos únicos
- Ratio de reuso: ~103 veces por descripción única
- Longitud promedio: 26.7 caracteres (mediana: 27)
- Palabras promedio: 4.4 palabras por descripción
- 89.49% de descripciones en rango ideal (20-35 caracteres)

**Top 5 Palabras Frecuentes:**
1. OF (40,804 apariciones)
2. SET (40,719 apariciones)
3. BAG (37,774 apariciones)
4. RED (31,813 apariciones)
5. HEART (28,979 apariciones)

### Atributos Extraíbles con Técnicas Tradicionales (Regex)

#### 1. Colores (26.46% cobertura)
15 colores detectados: RED (8.59%), PINK (5.20%), WHITE (4.07%), BLUE (3.64%), IVORY (1.68%), CREAM (1.65%), GREEN (1.55%), BLACK (1.42%), SILVER (1.22%), YELLOW (0.42%), PURPLE (0.25%), GREY (0.24%), ORANGE (0.23%), GOLD (0.21%), BROWN (0.16%)

#### 2. Materiales (18.72% cobertura)
13 materiales detectados: TIN (5.89%), WOOD (4.94%), METAL (4.01%), PAPER (2.75%), WOODEN (2.52%), GLASS (2.26%), CERAMIC (1.71%), ZINC (1.02%), COTTON (0.22%), WOOL (0.14%), KNITTED (0.12%), FABRIC (0.10%), PLASTIC (0.05%)

#### 3. Tamaños (10.53% cobertura)
6 tamaños detectados: JUMBO (3.89%), SMALL (2.60%), LARGE (1.87%), MINI (1.51%), GIANT (0.28%), MEDIUM (0.28%)

#### 4. Estilos/Temas (17.83% cobertura)
9 estilos detectados: RETROSPOT (6.62%), VINTAGE (6.43%), POLKADOT (2.21%), SPACEBOY (2.15%), SKULLS (1.70%), REGENCY (1.70%), PAISLEY (1.67%), WOODLAND (1.25%), UNION JACK (0.74%)

#### 5. Sets/Packs (8.41% cobertura)
- SET OF X: 21,288 registros
- PACK OF X: 10,776 registros
- BOX OF X: 1,409 registros

### Categorías Implícitas Detectadas (Keywords)

| Categoría | Registros | Cobertura |
|-----------|-----------|-----------|
| BAGS/STORAGE | 95,337 | 23.96% |
| KITCHEN/HOME | 74,176 | 18.64% |
| DECORATION | 49,317 | 12.39% |
| GARDEN | 48,208 | 12.12% |
| STATIONERY | 34,302 | 8.62% |
| CHRISTMAS | 19,715 | 4.95% |
| CHILDREN | 15,247 | 3.83% |
| CLOTHING/TEXTILE | 9,498 | 2.39% |

### Features Extraíbles con LLM (Inferencia Semántica)

**Necesidad:** 48.79% de registros (194,121) NO tienen atributos explícitos detectables con regex

**Features secundarios (requieren LLM):**
1. **Categoría jerárquica** (3 niveles): Macro > Categoría > Subcategoría
   - Ejemplo: Home > Kitchen > Drinkware
2. **Función/Uso**: decorative, functional, gift, seasonal
3. **Ocasión/Target**: Christmas, party, kids, garden, wedding
4. **Forma/Shape**: heart, star, round, square, animal
5. **Características especiales**: vintage, handmade, set, collectible

**Features derivados (post-procesamiento):**
6. Complejidad del producto (single/set/bundle)
7. Precio por unidad real (UnitPrice / cantidad_en_set)
8. Densidad de información (atributos_explícitos / palabras)
9. Categoría de precio (low/mid/high) por segmento
10. Seasonal_flag (boolean: es producto estacional?)

### Estrategia de Enriquecimiento

#### Fase 1: Feature Engineering Manual ✅ COMPLETADA (01/04/2026)
1. ✅ Extracción de color, material, tamaño, estilo, cantidad con regex
2. ✅ Flags binarios creados: `has_color`, `has_material`, `is_set`, etc.
3. ✅ Cobertura documentada y validada
4. ✅ 4 gráficos de visualización generados

**Output obtenido:** 
- 59.68% del dataset enriquecido con atributos básicos (superó expectativa del 40%)
- 3,877 productos con 58 columnas (50 nuevas columnas generadas)
- Archivo: `data/04_feature/productos_enriquecidos_regex.parquet` (108 KB)

#### Fase 2: Enriquecimiento con LLM (2-3 horas)
1. Exportar las 3,877 descripciones únicas
2. Procesar con Claude API en batches de 100-200 productos
3. Extraer: categoría jerárquica, función, ocasión, forma
4. Generar `data/04_feature/productos_enriquecidos.parquet`
5. Join con dataset principal

**Estimación de esfuerzo:**
- 39 batches de 100 productos
- ~117K tokens input + ~195K tokens output
- Costo estimado: ~$3.28 (Claude Sonnet 4.5)
- Tiempo: 2-3 horas (incluyendo rate limits y QA)

**Output esperado:** Tabla de mapping con 15 atributos nuevos por producto

#### Fase 3: Análisis Enriquecido
1. RFM + Product Affinity segmentation
2. Análisis de categorías de producto × comportamiento de cliente
3. Market basket analysis
4. CLV segmentado por tipo de producto preferido
5. Visualizaciones de segmentos por afinidad de producto

### Valor Analítico Esperado

**Segmentación avanzada:**
- Identificar segmentos por afinidad de producto (no solo RFM)
- Clientes "Christmas-focused" vs "Kitchen-focused" vs "Decoration-lovers"
- Detectar patrones cross-category o especializados

**Análisis de producto:**
- ¿Qué categorías generan más revenue?
- ¿Productos decorativos vs funcionales tienen diferentes tasas de cancelación?
- ¿Qué productos se compran juntos? (market basket)

**Insights temporales:**
- Estacionalidad por categoría (jardín en primavera, decoración navideña)
- Predicción de demanda por tipo de producto

**CLV segmentado:**
- Customer Lifetime Value por preferencia de categoría
- Identificar clientes high-value por tipo de producto

### Productos Problemáticos Detectados

**Descripciones genéricas/no-productos:**
- POSTAGE (1,099 transacciones, £77,803.96)
- Manual (284 transacciones, £53,779.93)
- DOTCOM POSTAGE (16 transacciones)

**Recomendación:** Filtrar o etiquetar como "No-Product" para análisis de productos reales.

### Archivos Generados (Enriquecimiento Fase 1)

- ✅ `notebooks/4-feat_eng/05-gc-product_enrichment_regex-2026_04_01.ipynb` - Notebook de enriquecimiento con regex
- ✅ `data/04_feature/productos_enriquecidos_regex.parquet` - 3,877 productos con 58 columnas
- ✅ `data/04_feature/rfm_clientes_enriched.parquet` - RFM + preferencias de producto por cliente
- ✅ `data/08_reporting/product_attributes_coverage.png` - Cobertura de atributos
- ✅ `data/08_reporting/product_attributes_distribution.png` - Distribución de n_attributes
- ✅ `data/08_reporting/top_colors_frequency.png` - Top 10 colores
- ✅ `data/08_reporting/top_materials_frequency.png` - Top 10 materiales

---

## Decisiones Técnicas Clave (Entrega 02)

### 1. Eliminación vs Imputación de CustomerID Nulos
**Decisión:** Eliminar 135,080 registros (24.9%)
**Justificación:** Imposible imputar IDs sin introducir ruido o duplicación artificial. El objetivo es segmentación por cliente.
**Impacto:** Dataset reducido a 397,884 registros, pero con calidad garantizada para análisis RFM.

### 2. Neteo de Cancelaciones en Monetary
**Decisión:** Monetary = Revenue_bruto - Revenue_cancelado (clipped a 0)
**Justificación:** Un cliente que compra $1000 pero cancela $900 tiene valor real de $100, no $1000.
**Impacto:** 13 clientes quedaron con Monetary=0 (cancelaron todo). Segmentación reflejará valor comercial real.

### 3. Cancel_rate como Feature Adicional
**Decisión:** Agregar Cancel_rate = (Revenue_cancelado / Revenue_bruto) × 100
**Justificación:** Tasa de cancelación indica comportamiento problemático/insatisfacción, independiente de RFM tradicional.
**Impacto:** Permite identificar clientes de riesgo en segmentación (correlación baja con R, F, M).

### 4. Separación de Cancelaciones
**Decisión:** Dataset separado `cancelaciones.parquet` en lugar de mezclar con ventas
**Justificación:** Facilita análisis independiente de patrones de cancelación y mantiene limpio el dataset de ventas.
**Impacto:** Pipeline más claro, análisis de cancelaciones por separado sin distorsionar métricas de ventas.

### 5. Formato Parquet para Almacenamiento
**Decisión:** Usar .parquet en lugar de .csv para datos limpios
**Justificación:** Compresión eficiente, preserva tipos de datos, lectura más rápida en pandas.
**Impacto:** Archivos 60% más pequeños que CSV equivalente, sin pérdida de información.

### 6. Justificación del Dataset en Notebook
**Decisión:** Agregar sección formal en notebook 01 explicando por qué se eligió Online Retail
**Justificación:** Requisito del PDF de Entrega 02, pero también contexto valioso para futuros revisores.
**Contenido:** 6 razones (relevancia RFM, datos reales, escala apropiada, complejidad, aplicabilidad, disponibilidad).

## Decisiones Técnicas Clave (Post-Feedback Entrega 01)

### 7. Enriquecimiento del Campo Description con Regex (Fase 1)
**Decisión:** Implementar pipeline híbrido (regex + LLM) para extraer atributos de productos
**Justificación:** Feedback de profesores señaló limitación de variables (solo 8 columnas). El campo `Description` contiene información latente estructurable que puede enriquecer el análisis significativamente.
**Impacto real (Fase 1 completada):**
- +50 atributos nuevos por producto (flags binarios, listas, métricas)
- 59.68% de productos enriquecidos con al menos 1 atributo
- Dataset preparado para segmentación avanzada por afinidad de producto
**Enfoque técnico implementado:**
- ✅ Fase 1 (01/04/2026): Regex para atributos explícitos (59.68% cobertura, superó expectativa)
  - 15 colores, 13 materiales, 6 tamaños, 9 estilos detectados
  - Identificación de sets/packs con cantidad
  - 4 visualizaciones generadas
- ⏳ Fase 2 (pendiente): Claude API para inferencia semántica (40.21% de productos restantes)
- ⏳ Fase 3 (pendiente): Análisis enriquecido con features combinados
**Costo/Tiempo Fase 1:** 0 costo (regex), ~2 horas de implementación
**Estado:** ✅ Fase 1 completada (01/04/2026) | ⏳ Fase 2-3 pendientes para Entrega 03

## Archivos de Referencia

### PDFs del Proyecto
- `[01] Propuesta de proyecto - Grupo 12 - Ecommerce.pdf`
- `[02] Recopilación y preparación de datos.pdf`
- `[03] Modelado y presentación de la solución.pdf`

### Documentos de la Materia
- `Ciencia de datos aplicada - Temario y contexto materia.txt`
- `Consignas unificadas del Trabajo Práctico - Entregas 01 a 03.txt`

## Contacto y Referencias

**Repositorio:** https://github.com/gonrc/segmentacion-clientes-ecommerce
**Documentación:** https://grupo-12-itba.github.io/segmentacion-clientes-ecommerce
**Template base:** [data-science-project-template](https://github.com/JoseRZapata/data-science-project-template)

---

## Problemas Conocidos y Soluciones

### ⚠️ Warnings de hashlib durante ejecución de notebooks
**Síntoma:**
```
ERROR:root:code for hash blake2b was not found.
ValueError: unsupported hash type blake2b
```

**Causa:** Python 3.11.9 vía pyenv con problema de compilación de OpenSSL (blake2b/blake2s)

**Impacto:** ⚠️ Son WARNINGS, no errores fatales. Los notebooks se ejecutan correctamente.

**Solución:** Ignorar los warnings. No afectan la funcionalidad de pandas, jupyter o nbconvert.

---

### ⚠️ UV no instalado en el sistema
**Síntoma:** `make install_env` falla con "uv: No such file or directory"

**Causa:** UV no está instalado en el sistema actual

**Solución aplicada:** Usar `python3 -m venv .venv` + `pip install` directamente

**Para instalar UV (opcional):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### ✅ Dataset no en repositorio (.gitignore)
**Comportamiento esperado:** Los archivos en `data/` NO se suben a GitHub

**Razón:** .gitignore tiene `data/**` para evitar subir archivos grandes (23MB xlsx, 3MB parquet)

**Qué está en GitHub:**
- ✅ Notebooks ejecutados con outputs completos (incluye visualizaciones embebidas)
- ✅ Estructura de carpetas vacía (con .gitkeep)

**Qué NO está en GitHub:**
- ❌ Online Retail.xlsx (23 MB)
- ❌ Archivos .parquet (3.2 MB total)
- ❌ Gráficos .png (10 archivos)

**Implicación:** Cualquiera que clone el repo debe descargar el dataset manualmente y ejecutar los notebooks.

---

### 📋 Ejecución de notebooks programática

**Script usado:**
```python
# execute_notebook.py
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def execute_notebook(notebook_path):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': str(notebook_path.parent.resolve())}})

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
```

**Uso:**
```bash
.venv/bin/python execute_notebook.py "notebooks/1-data/01-gc-carga_y_limpieza-2026_03_18.ipynb"
```

---

## Notas para Claude

### Estado Actual del Proyecto (03/04/2026)
- ✅ **Entrega 01:** Completada (propuesta presentada 25/03/2026)
- ✅ **Entrega 02:** Completada y actualizada con enriquecimiento (commits `b0264f6` + `b372c48`)
- ✅ **Feedback post-Entrega 01:** Enriquecer dataset - Fase 1 completada con regex (01/04/2026)
- ✅ **Enriquecimiento Fase 1:** Completado - 3,877 productos con 58 columnas (+50 nuevas)
- ✅ **Visualizaciones:** 14 gráficos totales (10 EDA + 4 enriquecimiento)
- 📅 **Presentación Entrega 02:** 29/04/2026 (en 26 días)
- ⏳ **Entrega 03:** Pendiente (fecha límite: 23/06/2026)
  - PRÓXIMO: Fase 2 enriquecimiento con LLM (opcional, 40% restante)
  - PRIORIDAD: Clustering y modelado con features enriquecidos

### Entorno de Desarrollo
- Python 3.11.9 vía pyenv (con warnings de hashlib que pueden ignorarse)
- Entorno virtual en `.venv/` (creado con venv estándar, NO con UV)
- Dependencias instaladas vía pip: pandas, openpyxl, pyarrow, matplotlib, seaborn, jupyter, nbconvert
- UV NO está instalado en el sistema, usar pip directamente

### Convenciones y Buenas Prácticas
- Priorizar notebooks sobre scripts para fases de análisis y exploración
- Seguir nomenclatura: `NN-<iniciales>-<tema>-YYYY_MM_DD.ipynb`
- Documentar decisiones en markdown cells (especialmente en secciones de Reflexión)
- Usar `make` si funciona, sino ejecutar comandos directamente
- Pipeline de datos: `01_raw` → `02_intermediate` → `03_primary` → `04_feature` → `05_model_input`

### Gestión de Datos
- **Los datos crudos en `data/01_raw/` NO se modifican nunca**
- Archivos en `data/` NO están en GitHub (.gitignore) - ✅ Comportamiento correcto
- El dataset debe descargarse manualmente: `curl -L -o data/01_raw/online_retail.zip https://archive.ics.uci.edu/static/public/352/online+retail.zip`
- Descomprimir: `unzip data/01_raw/online_retail.zip -d data/01_raw/`

### Git y GitHub
- Repositorio: https://github.com/gonrc/segmentacion-clientes-ecommerce
- Branch principal: `main`
- Pre-commit hooks configurados (ruff para linting)
- Commits deben ser descriptivos y seguir el formato: "Tipo: Descripción detallada"
- Los notebooks SE suben a GitHub con sus outputs completos (las visualizaciones están embebidas)

### Archivos Clave para Entrega 02
- `notebooks/ENTREGA02_CUMPLIMIENTO.md` - Checklist de cumplimiento al 100%
- Notebooks 01, 02, 04 ejecutados con datos reales
- Justificación del dataset en notebook 01, celda 2
- Reflexión final completa en notebook 04, última celda

### Archivos para Entrega 03

**Completados:**
- ✅ `notebooks/4-feat_eng/05-gc-product_enrichment_regex-2026_04_01.ipynb` - Enriquecimiento Fase 1 con regex
- ✅ `data/04_feature/productos_enriquecidos_regex.parquet` - 3,877 productos con 58 columnas
- ✅ `data/04_feature/rfm_clientes_enriched.parquet` - RFM + preferencias de producto

**Pendientes:**
- ⏳ `notebooks/4-feat_eng/06-gc-product_enrichment_llm-2026_XX_XX.ipynb` - Enriquecimiento Fase 2 con LLM (opcional)
- ⏳ `notebooks/5-models/07-gc-clustering_rfm_product-2026_XX_XX.ipynb` - Clustering con features enriquecidos
- ⏳ `notebooks/6-interpretation/08-gc-analisis_segmentos-2026_XX_XX.ipynb` - Interpretación de segmentos
- ⏳ `notebooks/7-deploy/09-gc-streamlit_app-2026_XX_XX.ipynb` - Prototipo interactivo

### Próximos Pasos (Entrega 03)

**PRIORIDAD 1: Enriquecimiento del Dataset ✅ COMPLETADA (Fase 1)**
1. ✅ Implementar extracción de atributos con regex (color, material, tamaño, estilo) - 01/04/2026
2. ⏳ Procesar 3,877 productos únicos con Claude API para categorización semántica (OPCIONAL - Fase 2)
3. ✅ Generar tabla `productos_enriquecidos_regex.parquet` con 50 nuevos atributos
4. ✅ Join con dataset principal y validación de calidad (rfm_clientes_enriched.parquet)

**PRIORIDAD 2: Feature Engineering Avanzado**
5. Estandarización de variables RFM (StandardScaler)
6. Product Affinity Matrix (qué productos compran juntos)
7. Features temporales (estacionalidad por categoría)
8. CLV estimado por segmento de producto

**PRIORIDAD 3: Modelado y Segmentación**
9. Clustering K-Means con features enriquecidos (determinar k óptimo con elbow + silueta)
10. Segmentación RFM + Product Affinity
11. Interpretación de segmentos (perfiles, etiquetas de negocio)
12. Validación con cohortes

**PRIORIDAD 4: Despliegue y Presentación**
13. Prototipo Streamlit/Flask con segmentación interactiva
14. Dashboard de análisis de producto
15. Documentación final y narrativa
16. Presentación oral (10-15 min): enfatizar enriquecimiento de datos como respuesta al feedback

### Ejecución de Notebooks
- **NO usar** `jupyter nbconvert --execute` directamente (puede fallar con paths relativos)
- **SÍ usar** el script `execute_notebook.py` que configura correctamente el contexto de ejecución
- Los warnings de hashlib (blake2b/blake2s) son normales y pueden ignorarse
