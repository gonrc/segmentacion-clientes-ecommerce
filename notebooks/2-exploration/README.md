# 2-exploration: Analisis Exploratorio de Datos (EDA)

## Que se hizo

Se analizo la base limpia de ventas para entender como se comportan las ventas, los clientes, los productos, los paises y las cancelaciones.

## Por que

Antes de construir features o modelos, es necesario entender los datos. El EDA permite detectar patrones, anomalias y oportunidades que guian las decisiones posteriores.

## Hallazgos principales

**Concentracion geografica:** United Kingdom representa ~82% del revenue. Los mercados secundarios (Alemania, Francia, Irlanda) son mucho mas chicos.

**Temporalidad:** Hay un pico claro de ventas entre septiembre y noviembre (temporada navidena). No se registran ventas los sabados. Las horas pico son entre las 10 y las 15hs.

**Concentracion de clientes (Pareto):** Un porcentaje reducido de clientes genera la mayor parte del ingreso. Esto valida la necesidad de segmentar.

**Productos:** Pocos productos concentran una parte significativa de la facturacion total.

**Cancelaciones:** Son ~8,900 lineas. Algunos clientes concentran muchas cancelaciones, lo que puede ser una senal para analisis de riesgo.

## Graficos generados

Los siguientes graficos se guardaron en `data/08_reporting/`:

- `dist_revenue.png` - Distribucion de revenue por linea y por cliente
- `revenue_por_pais.png` - Top 10 paises por revenue
- `evolucion_temporal.png` - Revenue, transacciones y clientes por mes
- `patrones_temporales.png` - Revenue por dia de semana y hora
- `top_productos.png` - Top 10 productos por revenue
- `pareto_clientes.png` - Curva de concentracion de revenue
- `cancelaciones_por_mes.png` - Evolucion temporal de cancelaciones
