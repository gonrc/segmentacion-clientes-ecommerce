# 4-feat_eng: Tabla RFM por cliente (con cancelaciones neteadas)

## Que se hizo

Se construyo una tabla con cuatro variables por cliente:

- **Recency**: cuantos dias pasaron desde la ultima compra del cliente.
- **Frequency**: cuantas transacciones distintas hizo el cliente.
- **Monetary**: cuanto gasto el cliente en total, **neto de cancelaciones** (revenue bruto menos el valor cancelado).
- **Cancel_rate**: porcentaje del revenue bruto que fue cancelado por el cliente.

## Por que

### Monetary neto en vez de bruto

La version anterior usaba el revenue bruto (solo ventas). Pero hay clientes que cancelan gran parte de sus compras. Por ejemplo, el cliente 16446 tiene $168k en ventas brutas pero cancelo $168k, quedando con solo $2.90 netos. Usar el bruto lo clasificaria como "top client" cuando en realidad no lo es.

Netear cancelaciones da una imagen real del valor de cada cliente.

### Cancel_rate como feature extra

La tasa de cancelacion no tiene correlacion fuerte con Recency, Frequency ni Monetary, lo que significa que agrega informacion nueva. Permite identificar clientes con comportamiento problematico que de otra forma pasarian desapercibidos.

## Que se obtuvo

Dos archivos Parquet en `data/04_feature/`:

| Archivo | Registros | Columnas |
|---------|-----------|----------|
| `rfm_clientes.parquet` | ~4,300 clientes | CustomerID, Recency, Frequency, Monetary, Cancel_rate |
| `rfm_clientes_detalle.parquet` | ~4,300 clientes | Idem + Monetary_bruto, Revenue_cancelado |

## Numeros clave

- 1,556 clientes (35.9%) tienen al menos una cancelacion
- Las cancelaciones representan ~$601k (6.7% del revenue bruto)
- 13 clientes quedaron con revenue neto negativo, llevados a $0
- Clientes extremos: algunos cancelaron casi el 100% de sus compras

## Graficos generados

En `data/08_reporting/`:

- `rfm_distribuciones.png` - Histogramas de Recency, Frequency, Monetary neto y Cancel_rate
- `rfm_correlacion.png` - Mapa de calor de correlaciones (ahora incluye Cancel_rate)
- `rfm_scatter.png` - Monetary bruto vs neto, y Frequency vs Cancel_rate
