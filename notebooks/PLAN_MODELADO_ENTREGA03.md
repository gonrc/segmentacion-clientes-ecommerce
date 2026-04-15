# Plan de Modelado - Entrega 03 (Componente 1)

**Fecha:** 2026-04-15
**Objetivo:** Implementar, validar y documentar los modelos para la Entrega 03
**Fecha límite:** 23/06/2026

---

## Enfoque General

Dos modelos complementarios que responden preguntas de negocio distintas:

| Modelo | Tipo | Pregunta que responde |
|--------|------|----------------------|
| **A. Clustering** | No supervisado (descriptivo) | ¿Qué segmentos de clientes tenemos? |
| **B. Predicción de churn** | Supervisado (clasificación) | ¿Qué clientes van a dejar de comprar? |

**Justificación del enfoque dual:**
- La consigna acepta modelos descriptivos, predictivos o ambos
- El curso cubre K-Means (U4) y Random Forest/LightGBM (U4), usar ambos demuestra dominio
- Clustering identifica segmentos; churn los hace accionables (retención dirigida)
- Los features enriquecidos (regex) aportan a ambos modelos

---

## Modelo A: Clustering de Clientes

### Objetivo
Segmentar los 4,338 clientes en grupos homogéneos usando RFM + atributos de producto.

### Datos de entrada
`data/04_feature/rfm_clientes_enriched.parquet` (4,338 clientes x 13 columnas)

**Features numéricos para clustering (10):**
- RFM: `Recency`, `Frequency`, `Monetary`, `Cancel_rate`
- Producto: `pct_with_color`, `color_diversity`, `pct_with_material`, `avg_quantity_in_set`, `pct_purchases_sets`
- Flag: `is_color_specialist` (binario)

**Features categóricos (no entran al modelo pero sirven para interpretar):**
- `dominant_color`, `dominant_material`

### Pipeline

#### Paso 1: Preparación
- Estandarizar features numéricos con `StandardScaler`
- No aplicar PCA salvo que las correlaciones altas lo justifiquen (Frequency-Monetary ~0.7 es tolerable)

#### Paso 2: Determinar k óptimo
- **Elbow method** (inertia vs k, para k=2..10)
- **Silhouette score** (para k=2..10)
- **Calinski-Harabasz index** (complementario)
- Elegir k en el rango 4-6 (balance entre granularidad y accionabilidad)

#### Paso 3: Entrenar K-Means
- `KMeans(n_clusters=k, random_state=42, n_init=10)`
- Asignar cluster a cada cliente

#### Paso 4: Interpretar segmentos
- Calcular centroide de cada cluster (valores promedio de cada feature)
- Visualizar con t-SNE o UMAP (2D)
- Asignar etiquetas de negocio descriptivas (ej: "VIP diversificado", "Ocasional especializado")
- Boxplots comparativos por feature y cluster
- Análisis de `dominant_color` y `dominant_material` por cluster

### Métricas de evaluación
- **Silhouette score** (target: > 0.25, ideal > 0.40)
- **Calinski-Harabasz index** (mayor = mejor)
- **Tamaño de clusters** (que no haya clusters degenerados con <2% de clientes)
- **Interpretabilidad** (los segmentos deben tener sentido comercial)

### Notebook
`notebooks/5-models/07-gc-clustering-2026_XX_XX.ipynb`

### Output
- `data/06_models/kmeans_model.pkl` (modelo serializado)
- `data/07_model_output/clientes_segmentados.parquet` (tabla con cluster asignado)
- Visualizaciones en `data/08_reporting/`

---

## Modelo B: Predicción de Churn

### Objetivo
Predecir si un cliente dejará de comprar en los próximos 3 meses.

### Definición de churn
- **Período de observación:** 2010-12-01 a 2011-08-31 (9 meses) - para calcular features
- **Período de predicción:** 2011-09-01 a 2011-12-09 (3 meses) - para definir target
- **Churn = 1:** Cliente compró en observación pero NO en predicción
- **Churn = 0:** Cliente compró en ambos períodos

**Balance esperado:** 41.2% churn / 58.8% retained (3,317 clientes en scope, balance razonable)

### Features
Se recalculan RFM y atributos de producto **solo con datos del período de observación** (evitar data leakage):

**RFM recalculado (4):**
- `Recency`: días desde última compra hasta 2011-08-31
- `Frequency`: cantidad de facturas únicas
- `Monetary`: revenue neto total
- `Cancel_rate`: tasa de cancelación

**Atributos de producto (5):**
- `pct_with_color`, `color_diversity`, `is_color_specialist`
- `pct_with_material`, `pct_purchases_sets`

**Features adicionales potenciales (4):**
- `avg_days_between_purchases`: regularidad de compra
- `months_active`: meses distintos con al menos una compra
- `n_products_unique`: diversidad de productos comprados
- `avg_order_value`: ticket promedio por factura

### Pipeline

#### Paso 1: Preparar dataset temporal
- Filtrar ventas pre 2011-09-01 para features
- Construir target binario con ventas post 2011-09-01
- Excluir clientes nuevos del período de predicción (no tienen historia)

#### Paso 2: Split train/test
- **Stratified split 80/20** (mantener proporción de churn)
- No usar split temporal adicional (ya hay split temporal en la definición del target)

#### Paso 3: Entrenar modelos
Probar al menos 2 algoritmos para comparar:

1. **Random Forest** (`RandomForestClassifier`)
   - Baseline robusto, interpretable via feature importance
   - Grid search: `n_estimators`, `max_depth`, `min_samples_leaf`

2. **LightGBM** (`LGBMClassifier`) - si se instala, sino usar `GradientBoostingClassifier` de sklearn
   - Generalmente mejor performance
   - Grid search: `n_estimators`, `learning_rate`, `max_depth`

#### Paso 4: Evaluar
- **Cross-validation 5-fold** stratificado para seleccionar el mejor modelo
- Evaluar en test set con métricas finales

#### Paso 5: Interpretar
- Feature importance (top 10 features)
- Análisis de errores: ¿qué tipo de clientes clasifica mal?
- Cruzar predicciones de churn con segmentos del clustering

### Métricas de evaluación
- **F1-score** (métrica principal, balancea precision y recall)
- **AUC-ROC** (capacidad discriminativa general)
- **Precision y Recall por clase** (entender trade-offs)
- **Matriz de confusión** (visualización de errores)
- **Classification report completo**

### Notebook
`notebooks/5-models/08-gc-churn-2026_XX_XX.ipynb`

### Output
- `data/06_models/churn_model.pkl` (mejor modelo serializado)
- `data/07_model_output/churn_predictions.parquet` (predicciones)
- Visualizaciones en `data/08_reporting/`

---

## Análisis Combinado: Segmentos + Churn

Cruzar los resultados de ambos modelos en un análisis final:
- Tasa de churn por segmento (¿qué segmentos son más riesgosos?)
- Perfil del cliente en riesgo por segmento
- Recomendaciones de negocio diferenciadas por segmento

### Notebook
`notebooks/6-interpretation/09-gc-analisis_segmentos-2026_XX_XX.ipynb`

---

## Reflexión (requerida por la consigna)

Documentar en el notebook de interpretación:
- Por qué se eligió clustering + churn (justificación del enfoque dual)
- Limitaciones del dataset (12 meses, sesgo UK, falta de datos demográficos)
- Qué funcionó y qué no (métricas vs expectativas)
- Mejoras posibles (más datos, features externos, otros algoritmos)
- Cómo los resultados informan decisiones de negocio

---

## Resumen de Entregables

| Notebook | Contenido |
|----------|-----------|
| `07-gc-clustering-2026_XX_XX.ipynb` | K-Means: preparación, selección k, entrenamiento, interpretación |
| `08-gc-churn-2026_XX_XX.ipynb` | Churn: features temporales, RF/LightGBM, evaluación |
| `09-gc-analisis_segmentos-2026_XX_XX.ipynb` | Cruce segmentos+churn, reflexión final |

| Archivo | Ubicación |
|---------|-----------|
| Modelo K-Means | `data/06_models/kmeans_model.pkl` |
| Modelo Churn | `data/06_models/churn_model.pkl` |
| Clientes segmentados | `data/07_model_output/clientes_segmentados.parquet` |
| Predicciones churn | `data/07_model_output/churn_predictions.parquet` |

---

## Orden de Ejecución

1. **Notebook 07** - Clustering (no depende de nada nuevo)
2. **Notebook 08** - Churn (requiere recalcular features con split temporal)
3. **Notebook 09** - Análisis combinado (depende de 07 y 08)

## Dependencias a Instalar

```bash
pip install lightgbm  # opcional, se puede usar GradientBoostingClassifier como alternativa
```

Todas las demás dependencias (scikit-learn, scipy, pandas, matplotlib, seaborn) ya están instaladas.
