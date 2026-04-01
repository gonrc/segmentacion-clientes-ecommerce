# Decisión: Enriquecimiento del Dataset

**Fecha:** 2026-04-01
**Estado:** ✅ FASE 1 COMPLETADA (Regex)

## Análisis Realizado


📊 MÉTRICAS CLAVE:

COBERTURA:
  • Productos enriquecidos: 2,314 de 3,877 (59.7%)
  • Revenue capturado: $5.77M de $8.91M (64.7%)
  • Clientes alcanzados: 4,286 de 4,338 (98.8%)
  
ATRIBUTOS EXTRAÍDOS:
  • 58 flags binarios creados (15 colores + 13 materiales + 6 tamaños + 9 estilos + agregados)
  • Color: 34.2% de productos (vs 26.5% esperado a nivel transacción)
  • Material: 15.7% de productos
  • Tamaño: 8.4% de productos
  • Estilo: 13.5% de productos
  • Sets: 5.0% de productos
  
PODER DISCRIMINATORIO:
  • 94.4% de clientes compraron productos con color detectado
  • 90.0% de clientes compraron productos con material detectado
  • Diversidad promedio: 5.6 colores por cliente
  • 34.3% clientes especializados (≤3 colores)
  • 35.2% clientes generalistas (≥7 colores)
  
PRODUCTOS SIN ATRIBUTOS:
  • 1,559 productos (40.2%) sin atributos detectados
  • Representan $3.14M (35.3%) del revenue
  • Palabras comunes: SET, HEART, DESIGN, BOX, WALL, ART, CHRISTMAS
  • Categorías potenciales: LIGHTING (141), DOOR/WALL (123), KITCHEN (87), DECORATIVE (80)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ DECISIÓN RECOMENDADA: REGEX ES SUFICIENTE

RAZONES:
  1. 98.8% de cobertura de clientes (solo 52 clientes sin atributos)
  2. 64.7% de revenue capturado con atributos explícitos
  3. Flags binarios tienen alto poder discriminatorio para segmentación
  4. Los productos sin atributos son más difusos (no tienen patrones claros)
  5. Tiempo/costo de LLM no justificado para 35% adicional de revenue

ALTERNATIVAS CONSIDERADAS:
  ❌ Agregar más keywords regex → Rendimientos decrecientes (palabras muy específicas)
  ❌ LLM completo (1,559 productos) → $3.28, 2-3 horas, solo 35% adicional
  ✅ Proceder con RFM + Atributos regex para clustering

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PRÓXIMOS PASOS (Entrega 03):

FASE 2: FEATURE ENGINEERING CLIENTE-PRODUCTO
  1. Crear perfil de cliente por preferencias de atributos
     → % de compras por color/material/tamaño
     → Diversidad (Shannon entropy de colores)
     → Especialización (Gini index)
  
  2. Agregar features derivados a tabla RFM
     → dominant_color, dominant_material
     → color_diversity, material_diversity
     → is_color_specialist, is_generalista
     → avg_quantity_in_set (compra sets vs productos individuales)

FASE 3: CLUSTERING RFM + ATRIBUTOS
  3. Estandarizar variables (StandardScaler)
  4. K-Means con k=4-7 clusters
  5. Interpretar segmentos con perfiles de atributos
     → Ej: "Clientes RED-specialists de Alto Valor"
     → Ej: "Generalistas frecuentes de ticket bajo"

FASE 4: VALIDACIÓN Y DESPLIEGUE
  6. Métricas de calidad (silhouette, calinski-harabasz)
  7. Prototipo Streamlit con segmentación interactiva
  8. Documentación y presentación final

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
