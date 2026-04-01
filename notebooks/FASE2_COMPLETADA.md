# Fase 2 Completada: Feature Engineering Cliente-Producto

**Fecha:** 2026-04-01  
**Estado:** ✅ COMPLETADA

## Archivos Generados

1. **Notebook:** `notebooks/4-feat_eng/06-gc-customer_product_profile-2026_04_01.ipynb`
2. **Dataset:** `data/04_feature/rfm_clientes_enriched.parquet` (4,338 clientes × 13 columnas)

## Features Creadas

### Preferencias de Color
- `dominant_color`: Color más comprado por cliente
- `pct_with_color`: % de compras con color detectado
- `color_diversity`: Shannon entropy (0-3.17, mayor = más diverso)
- `is_color_specialist`: Boolean (diversity ≤ 1.0)

### Preferencias de Material
- `dominant_material`: Material más comprado
- `pct_with_material`: % de compras con material detectado

### Preferencias de Sets
- `avg_quantity_in_set`: Promedio de cantidad en sets comprados
- `pct_purchases_sets`: % de compras que son sets

## Hallazgos Clave

**Correlaciones:**
- `color_diversity` ↔ Recency: **-0.28** (clientes recientes más especializados)
- `color_diversity` ↔ Frequency: **+0.26** (frecuentes más diversos)
- Atributos de producto **NO correlacionan fuerte** con RFM → aportan info nueva

**Distribuciones:**
- Diversidad promedio: 1.74 colores (escala 0-3.17)
- 24.5% de clientes son especialistas de color
- Color dominante: RED (2,208 clientes), PINK (780), WHITE (611)
- Material dominante: TIN (1,069), METAL (867), PAPER (746)

## Validación

✅ Correlaciones bajas con RFM → features ortogonales  
✅ Distribuciones razonables (sin outliers extremos)  
✅ Poder discriminatorio alto (especialistas vs generalistas)  
✅ Listos para clustering K-Means

## Próxima Fase

**Fase 3: Clustering RFM + Atributos**
1. Estandarizar variables (StandardScaler)
2. Determinar k óptimo (elbow + silhouette)
3. K-Means con k=4-6
4. Interpretar segmentos con perfiles
5. Validar con métricas de calidad
