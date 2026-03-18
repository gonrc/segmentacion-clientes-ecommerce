# 1-data: Carga y limpieza del dataset

## Que se hizo

Se cargo el dataset crudo `Online Retail.xlsx` (541,909 transacciones) y se lo limpio para dejarlo listo para analisis.

## Por que

El dataset tiene varios problemas de calidad que impiden usarlo directamente:
- 135,080 registros (24.9%) no tienen CustomerID, lo que hace imposible atribuirlos a un cliente para segmentacion.
- Hay ~9,300 cancelaciones (invoices con prefijo "C") mezcladas con ventas normales.
- Existen registros con precios o cantidades invalidas (ceros, negativos).
- Las columnas StockCode e InvoiceNo tienen tipos mixtos (strings e integers mezclados).

## Que se obtuvo

Dos archivos Parquet en `data/03_primary/`:

| Archivo | Registros | Descripcion |
|---------|-----------|-------------|
| `ventas_limpias.parquet` | ~397,000 | Ventas validas con columna Revenue calculada |
| `cancelaciones.parquet` | ~8,900 | Cancelaciones separadas para analisis aparte |

## Criterios de limpieza

1. Se eliminaron registros sin CustomerID
2. Se separaron cancelaciones (InvoiceNo con prefijo "C")
3. Se filtraron Quantity <= 0 y UnitPrice <= 0
4. Se normalizaron tipos de datos
5. Se creo la columna `Revenue = Quantity * UnitPrice`
