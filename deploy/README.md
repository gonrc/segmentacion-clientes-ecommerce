# Despliegue de la solución — Entrega 04

Solución desplegada en dos servicios desacoplados que se comunican por HTTP:

| Servicio | Tecnología | Rol | URL local |
|----------|-----------|-----|-----------|
| **API** | FastAPI + Uvicorn | Capa de servicio: expone los modelos de la Entrega 03 | http://localhost:8000 (docs en `/docs`) |
| **Interfaz** | Streamlit | Consume la API para scorear clientes nuevos | http://localhost:8501 |

```
┌───────────────┐   POST /predict        ┌─────────────────────────┐
│  Streamlit    │ ─────────────────────▶ │  API REST (FastAPI)     │
│  (interfaz)   │ ◀───────────────────── │  api/main.py            │
└───────────────┘   JSON (segmento+churn)└───────────┬─────────────┘
                                                      │ usa
                                          ┌───────────▼─────────────┐
                                          │ src/inference/          │
                                          │   model_service.py      │  (lógica de modelo)
                                          └───────────┬─────────────┘
                                                      │ carga
                                          data/06_models/*.pkl + cluster_labels.json
```

La **separación lógica de modelo / capa de servicio** es explícita:
- `src/inference/model_service.py` — lógica pura de inferencia, sin HTTP.
- `api/` — capa de servicio (routing, validación de entradas/salidas, errores HTTP).

## Opción 1: Docker (recomendada)

Requiere Docker + Docker Compose, y los artefactos de la Entrega 03 en `data/06_models/`
(`kmeans_model.pkl`, `churn_model.pkl`, `cluster_labels.json`) y los parquets en `data/`.

> `cluster_labels.json` (mapeo cluster→segmento que usa la API) se deriva de
> `clientes_segmentados.parquet`. Si no existe, regeneralo con:
> `uv run python deploy/build_cluster_labels.py`

```bash
docker compose -f deploy/docker-compose.yml up --build
```

- API: http://localhost:8000/docs
- Interfaz: http://localhost:8501

Para frenar: `docker compose -f deploy/docker-compose.yml down`.

## Opción 2: Local sin Docker (uv)

En dos terminales, desde la raíz del repo:

```bash
# Terminal 1 — API
uv run uvicorn api.main:app --reload --port 8000

# Terminal 2 — Interfaz (apunta a la API por API_URL)
API_URL=http://localhost:8000 uv run streamlit run notebooks/7-deploy/streamlit_app.py
```

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Liveness + estado de carga de modelos |
| GET | `/metadata` | Features esperadas, segmentos y umbrales de riesgo |
| POST | `/predict` | Scoring combinado: segmento + churn + recomendación |
| POST | `/predict/churn` | Solo probabilidad y nivel de riesgo de churn |
| POST | `/predict/segment` | Solo segmento (cluster + etiqueta) |
| POST | `/predict/batch` | Scoring combinado para una lista de clientes |

### Ejemplo de uso

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Recency": 23, "Frequency": 9, "Monetary": 4200,
       "Cancel_rate": 0.03, "pct_with_color": 0.45}'
```

Respuesta:

```json
{
  "cluster": 2,
  "segment_label": "VIP",
  "segment_description": "Clientes de alto valor, alta frecuencia y mayor participación en revenue.",
  "churn_probability": 0.13,
  "churn_prediction": 0,
  "risk_level": "Bajo",
  "recommendation": "Riesgo Bajo. Mantener comunicación regular y beneficios livianos. Retención prioritaria: ..."
}
```

Solo `Recency`, `Frequency` y `Monetary` son obligatorias; el resto toma default 0.0.

## Tests

```bash
uv run pytest tests/test_api.py tests/inference/test_model_service.py -v
```

Los tests se saltean automáticamente si faltan los artefactos en `data/06_models/`.
