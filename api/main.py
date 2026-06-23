"""Capa de servicio: API REST que expone los modelos de la Entrega 03.

Responsabilidad acotada: validar entradas/salidas (Pydantic), enrutar las requests
hacia la **capa de lógica de modelo** (``src.inference.model_service.ModelService``)
y manejar errores con códigos HTTP claros. No contiene lógica de modelo.

Ejecutar local:
    uvicorn api.main:app --reload --port 8000
Docs interactivas: http://localhost:8000/docs
"""

from __future__ import annotations

import logging
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Permite importar la capa de modelo (src/) tanto en local como en el contenedor.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.schemas import (  # noqa: E402
    BatchScoreRequest,
    BatchScoreResponse,
    ChurnResponse,
    CustomerFeatures,
    HealthResponse,
    ScoreResponse,
    SegmentResponse,
)
from src.inference.model_service import ModelNotLoadedError, ModelService  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")
logger = logging.getLogger("api.scoring")

# Estado del proceso: el servicio de modelos se carga una sola vez al arrancar.
_state: dict[str, Any] = {"service": None, "error": None}


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    models_dir = os.getenv("MODELS_DIR")
    try:
        _state["service"] = ModelService(models_dir=models_dir)
        _state["error"] = None
        logger.info(
            "Modelos cargados correctamente (%s)", _state["service"].metadata()["model_version"]
        )
    except ModelNotLoadedError as exc:
        # No abortamos el arranque: /health reporta el problema y los endpoints
        # de predicción devuelven 503 con un mensaje claro.
        _state["service"] = None
        _state["error"] = str(exc)
        logger.warning("No se pudieron cargar los modelos: %s", exc)
    yield
    _state.clear()


app = FastAPI(
    title="API de Segmentación y Churn - Grupo 12",
    description=(
        "Servicio de scoring para e-commerce (dataset Online Retail). Expone los modelos "
        "de segmentación (K-Means) y de predicción de churn (Random Forest) entrenados "
        "en la Entrega 03."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# La interfaz Streamlit corre en otro origen/puerto: habilitamos CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_service() -> ModelService:
    """Devuelve el servicio cargado o levanta 503 si los modelos no están disponibles."""
    service: ModelService | None = _state.get("service")
    if service is None:
        detail = _state.get("error") or "Modelos no cargados."
        raise HTTPException(status_code=503, detail=detail)
    return service


@app.get("/", tags=["info"])
def root() -> dict[str, Any]:
    return {
        "service": "API de Segmentación y Churn - Grupo 12",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "GET /health",
            "GET /metadata",
            "POST /predict/churn",
            "POST /predict/segment",
            "POST /predict",
            "POST /predict/batch",
        ],
    }


@app.get("/health", response_model=HealthResponse, tags=["info"])
def health() -> HealthResponse:
    service = _state.get("service")
    if service is None:
        return HealthResponse(
            status="degraded",
            models_loaded=False,
            detail=_state.get("error"),
        )
    return HealthResponse(status="ok", models_loaded=True)


@app.get("/metadata", tags=["info"])
def metadata() -> dict[str, Any]:
    return get_service().metadata()


@app.post("/predict/churn", response_model=ChurnResponse, tags=["predict"])
def predict_churn(features: CustomerFeatures) -> ChurnResponse:
    service = get_service()
    try:
        result = service.predict_churn(features.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error de inferencia (churn): {exc}") from exc
    return ChurnResponse(**result)


@app.post("/predict/segment", response_model=SegmentResponse, tags=["predict"])
def predict_segment(features: CustomerFeatures) -> SegmentResponse:
    service = get_service()
    try:
        result = service.predict_segment(features.model_dump())
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Error de inferencia (segmento): {exc}"
        ) from exc
    return SegmentResponse(**result)


@app.post("/predict", response_model=ScoreResponse, tags=["predict"])
def predict(features: CustomerFeatures) -> ScoreResponse:
    service = get_service()
    try:
        result = service.score_customer(features.model_dump())
    except Exception as exc:
        logger.exception("Error de inferencia en /predict")
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {exc}") from exc
    logger.info(
        "/predict -> segmento=%s churn=%.3f riesgo=%s",
        result["segment_label"],
        result["churn_probability"],
        result["risk_level"],
    )
    return ScoreResponse(**result)


@app.post("/predict/batch", response_model=BatchScoreResponse, tags=["predict"])
def predict_batch(request: BatchScoreRequest) -> BatchScoreResponse:
    service = get_service()
    try:
        results = [
            ScoreResponse(**service.score_customer(customer.model_dump()))
            for customer in request.customers
        ]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error de inferencia (batch): {exc}") from exc
    return BatchScoreResponse(results=results)
