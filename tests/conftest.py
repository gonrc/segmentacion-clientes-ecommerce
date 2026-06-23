"""Configuración compartida de los tests de la API y la capa de modelo (Entrega 04)."""

from __future__ import annotations

import os

# Limitar los hilos de BLAS/OMP antes de importar sklearn/scipy evita cuelgues de
# inicialización del thread-pool en entornos restringidos (sandbox/CI).
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "data" / "06_models"
REQUIRED_ARTIFACTS = ["kmeans_model.pkl", "churn_model.pkl", "cluster_labels.json"]

# Si faltan los artefactos serializados (no están en git), se saltean los tests que
# los necesitan en vez de fallar.
_missing = [name for name in REQUIRED_ARTIFACTS if not (MODELS_DIR / name).exists()]
requires_models = pytest.mark.skipif(
    bool(_missing),
    reason=f"Faltan artefactos de modelo en {MODELS_DIR}: {', '.join(_missing)}",
)


@pytest.fixture
def sample_features() -> dict[str, float]:
    """Cliente VIP de ejemplo (alta frecuencia, alto Monetary, baja recencia)."""
    return {
        "Recency": 23,
        "Frequency": 9,
        "Monetary": 4200.0,
        "Cancel_rate": 2.0,
        "pct_with_color": 45.0,
        "color_diversity": 3.2,
        "is_color_specialist": 0,
        "pct_with_material": 18.0,
        "pct_purchases_sets": 22.0,
        "avg_quantity_in_set": 4.0,
        "avg_days_between_purchases": 28.0,
        "months_active": 8.0,
        "n_products_unique": 64,
        "avg_order_value": 320.0,
    }


@pytest.fixture(scope="session")
def service():
    from src.inference.model_service import ModelService

    return ModelService()


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as test_client:
        yield test_client
