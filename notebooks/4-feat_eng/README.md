# 4-feat_eng: Tabla RFM por cliente

## Que se hizo

Se construyo una tabla con tres variables por cliente a partir de la base limpia de ventas:

- **Recency**: cuantos dias pasaron desde la ultima compra del cliente.
- **Frequency**: cuantas transacciones distintas hizo el cliente.
- **Monetary**: cuanto gasto el cliente en total.

## Por que

RFM es la tecnica estandar para segmentar clientes en retail y e-commerce. Permite resumir todo el historial transaccional de un cliente en tres numeros simples e interpretables. Con esta tabla se puede aplicar clustering (K-Means, etc.) para identificar segmentos como "clientes de alto valor", "clientes inactivos", "compradores frecuentes", etc.

## Que se obtuvo

Un archivo Parquet en `data/04_feature/`:

| Archivo | Registros | Columnas |
|---------|-----------|----------|
| `rfm_clientes.parquet` | ~4,300 clientes | CustomerID, Recency, Frequency, Monetary |

## Hallazgos clave

- Frequency y Monetary tienen correlacion positiva alta: quien compra mas seguido, gasta mas.
- Recency tiene correlacion negativa: clientes recientes tienden a ser mas activos.
- Las tres variables estan muy sesgadas (muchos clientes con valores bajos, pocos con valores muy altos), lo que justifica escalar antes de aplicar clustering.

## Graficos generados

En `data/08_reporting/`:

- `rfm_distribuciones.png` - Histogramas de Recency, Frequency y Monetary
- `rfm_correlacion.png` - Mapa de calor de correlaciones entre variables RFM
- `rfm_scatter.png` - Scatter plots Recency vs Monetary y Frequency vs Monetary
