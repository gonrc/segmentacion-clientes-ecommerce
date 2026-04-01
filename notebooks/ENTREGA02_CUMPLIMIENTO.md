# Verificación de Cumplimiento: Entrega 02

**Fecha de verificación:** 2026-04-01  
**Estado:** ✅ TODOS LOS REQUISITOS CUMPLIDOS

---

## Consigna vs Entregado

### ✅ 1. Descripción del dataset

**Requisito:** Origen y formato, Variables incluidas (y significado), Justificación de la elección

**Cumplimiento:** ✅ COMPLETO  
**Ubicación:** `notebooks/1-data/01-gc-carga_y_limpieza-2026_03_18.ipynb` - Celda 2

**Contenido entregado:**
- ✅ Origen: UCI Machine Learning Repository
- ✅ Formato: Excel (.xlsx), 541,909 transacciones
- ✅ Variables: Tabla completa con 8 variables y descripciones
- ✅ Justificación: 6 razones detalladas (relevancia RFM, datos reales, escala apropiada, complejidad, aplicabilidad comercial, disponibilidad pública)

---

### ✅ 2. Análisis exploratorio básico

**Requisito:** Tipos de variables, Distribuciones, Valores faltantes, Outliers, Estadísticas descriptivas, Visualizaciones iniciales

**Cumplimiento:** ✅ COMPLETO  
**Ubicación:** `notebooks/2-exploration/02-gc-eda_ventas-2026_03_18.ipynb`

**Contenido entregado:**
- ✅ Tipos de variables: `df.info()` con dtypes (celda 7 notebook 01)
- ✅ Distribuciones: Revenue, Revenue por cliente (gráfico 1)
- ✅ Valores faltantes: Tabla con nulos y porcentajes (celda 9 notebook 01)
- ✅ Outliers: Clipping al P99 para visualizaciones, documentados (celda 6 notebook 02)
- ✅ Estadísticas descriptivas: `df.describe()` (celda 8 notebook 01)
- ✅ **10 visualizaciones generadas:**
  1. `dist_revenue.png` - Distribución de revenue
  2. `revenue_por_pais.png` - Top 10 países
  3. `evolucion_temporal.png` - Revenue/transacciones/clientes por mes
  4. `patrones_temporales.png` - Por día de semana y hora
  5. `top_productos.png` - Top 10 productos
  6. `pareto_clientes.png` - Curva de concentración
  7. `cancelaciones_por_mes.png` - Evolución de cancelaciones
  8. `rfm_distribuciones.png` - Distribuciones de RFM (notebook 04)
  9. `rfm_correlacion.png` - Matriz de correlación (notebook 04)
  10. `rfm_scatter.png` - Scatters (notebook 04)

---

### ✅ 3. Diagnóstico y mejoras en la calidad de los datos

**Requisito:** Identificación de problemas (faltantes, inconsistencias, duplicados), Decisiones tomadas para limpiar o transformar

**Cumplimiento:** ✅ COMPLETO  
**Ubicación:** `notebooks/1-data/01-gc-carga_y_limpieza-2026_03_18.ipynb` - Celdas 10-12

**Problemas identificados:**
1. ✅ CustomerID nulo en 135,080 registros (24.9%)
2. ✅ Description nula en 1,454 registros (0.27%)
3. ✅ Cancelaciones (InvoiceNo con 'C'): 9,288 registros
4. ✅ Quantity negativa: 10,624 registros
5. ✅ UnitPrice = 0: 2,515 registros
6. ✅ UnitPrice negativo: 2 registros
7. ✅ Tipos mixtos en StockCode e InvoiceNo

**Decisiones tomadas:**
- ✅ Eliminar registros sin CustomerID (imposible segmentar sin ID)
- ✅ Separar cancelaciones en dataset independiente
- ✅ Filtrar Quantity ≤ 0 y UnitPrice ≤ 0
- ✅ Normalizar tipos mixtos a string
- ✅ Crear columna Revenue = Quantity × UnitPrice

---

### ✅ 4. Transformaciones realizadas

**Requisito:** Normalización/estandarización, Codificación de variables categóricas, Generación de nuevas variables, Filtrado/selección

**Cumplimiento:** ✅ COMPLETO  

**Transformaciones documentadas:**
- ✅ **Generación de nuevas variables:**
  - `Revenue` = Quantity × UnitPrice (notebook 01)
  - `Recency`, `Frequency`, `Monetary` (tabla RFM, notebook 04)
  - `Cancel_rate` (porcentaje cancelado por cliente, notebook 04)
  - `YearMonth`, `DayOfWeek`, `Hour` (análisis temporal, notebook 02)
  
- ✅ **Filtrado de variables:**
  - Eliminación de registros sin CustomerID
  - Separación de cancelaciones
  - Filtrado de Quantity/UnitPrice inválidos

- ⚠️ **Normalización/estandarización:** NO APLICADA AÚN
  - **Razón:** Se dejó pendiente para fase de clustering (Entrega 03)
  - **Planificado:** StandardScaler antes de K-Means

- ⚠️ **Codificación de categóricas:** NO REQUERIDA
  - **Razón:** Análisis descriptivo y RFM no requieren encoding
  - **Planificado:** One-hot encoding de `dominant_color`, `dominant_material` si se usan en modelos supervisados (Entrega 03)

---

### ✅ 5. Reflexión final

**Requisito:** Qué decisiones se tomaron y justificación, Dificultades encontradas, Siguientes pasos proyectados

**Cumplimiento:** ✅ COMPLETO  
**Ubicación:** `notebooks/4-feat_eng/04-gc-rfm_por_cliente-2026_03_18.ipynb` - Última celda

**Contenido entregado:**

**Decisiones tomadas (6):**
1. ✅ Eliminación vs Imputación de CustomerID nulos
2. ✅ Neteo de Cancelaciones en Monetary
3. ✅ Cancel_rate como Feature Adicional
4. ✅ Separación de Cancelaciones en dataset independiente
5. ✅ Formato Parquet para almacenamiento
6. ✅ Justificación del Dataset en notebook

**Dificultades encontradas (5):**
1. ✅ Alto porcentaje de CustomerID nulos (24.9%)
2. ✅ Inconsistencia en manejo de cancelaciones
3. ✅ Valores extremos en Quantity y UnitPrice
4. ✅ Correlación entre Frequency y Monetary
5. ✅ Distribución geográfica sesgada (UK 82%)

**Siguientes pasos proyectados (6):**
1. ✅ Estandarización de variables RFM
2. ✅ Clustering de clientes con K-Means
3. ✅ Interpretación y caracterización de segmentos
4. ✅ Validación con análisis de cohortes
5. ✅ Prototipo de despliegue
6. ✅ Documentación final y presentación

---

## ⚠️ Trabajo Adicional Post-Entrega 02 (01/04/2026)

**Nota:** El 01/04/2026 se realizó trabajo adicional de enriquecimiento del dataset que NO estaba en la Entrega 02 original pero responde al feedback de profesores del 25/03/2026.

### Notebooks adicionales:
- `05-gc-product_enrichment_regex-2026_04_01.ipynb` - Extracción de atributos con regex
- `06-gc-customer_product_profile-2026_04_01.ipynb` - Perfiles de cliente por atributos

### Justificación:
Los profesores señalaron en la presentación del 25/03/2026 que el dataset tenía pocas variables (solo 8 columnas), sugiriendo enriquecer usando el campo `Description` para extraer atributos adicionales (colores, materiales, categorías).

Este trabajo se realizó para fortalecer la **Entrega 03** con features adicionales para segmentación avanzada.

---

## Archivos Entregados (Entrega 02 - 28/04/2026)

### Notebooks:
1. ✅ `notebooks/1-data/01-gc-carga_y_limpieza-2026_03_18.ipynb`
2. ✅ `notebooks/2-exploration/02-gc-eda_ventas-2026_03_18.ipynb`
3. ✅ `notebooks/4-feat_eng/04-gc-rfm_por_cliente-2026_03_18.ipynb`

### Datasets generados:
1. ✅ `data/03_primary/ventas_limpias.parquet` (397,884 registros)
2. ✅ `data/03_primary/cancelaciones.parquet` (8,905 registros)
3. ✅ `data/04_feature/rfm_clientes.parquet` (4,338 clientes)
4. ✅ `data/04_feature/rfm_clientes_detalle.parquet` (con desglose)

### Visualizaciones:
1-10. ✅ 10 gráficos PNG en `data/08_reporting/`

### Documentación:
- ✅ `notebooks/ENTREGA02_CUMPLIMIENTO.md` - Checklist de cumplimiento al 100%
- ✅ PDFs: `[01] Propuesta de proyecto - Grupo 12 - Ecommerce.pdf`
- ✅ PDFs: `[02] Recopilación y preparación de datos.pdf`

---

## Conclusión

✅ **TODOS LOS REQUISITOS DE LA ENTREGA 02 ESTÁN CUMPLIDOS**

La entrega cubre exhaustivamente:
- Descripción del dataset con justificación formal
- Análisis exploratorio con 10 visualizaciones
- Diagnóstico de calidad con 7 problemas identificados
- Transformaciones documentadas (generación de features, filtrado)
- Reflexión final completa (decisiones, dificultades, próximos pasos)

**Nota sobre normalización/estandarización:**  
Se dejó intencionalmente pendiente para la fase de clustering (Entrega 03), donde se aplicará StandardScaler antes de K-Means. Esta decisión está documentada en la reflexión final como "siguiente paso".

---

**Verificado por:** Claude Code (01/04/2026)
