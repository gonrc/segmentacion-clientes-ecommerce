"""Tests de la capa de servicio (API REST FastAPI)."""

from __future__ import annotations

import pytest

from tests.conftest import requires_models

pytestmark = requires_models

VALID_SEGMENTS = {"VIP", "Compradores de Sets", "En Riesgo", "Dormidos"}


def test_health_ok(client) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["models_loaded"] is True


def test_metadata(client) -> None:
    resp = client.get("/metadata")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["required_features"]) == 14
    # Versión de modelo y rangos por feature (MLOps / validación informada)
    assert "model_version" in body
    assert "feature_ranges" in body and "Monetary" in body["feature_ranges"]


def test_predict_includes_model_version(client, sample_features) -> None:
    body = client.post("/predict", json=sample_features).json()
    assert body["model_version"]


def test_vip_profile_is_labeled_vip(client) -> None:
    """Un perfil claramente de alto valor (reciente, frecuente, alto gasto) cae en VIP."""
    vip = {"Recency": 10, "Frequency": 30, "Monetary": 20000, "pct_purchases_sets": 5}
    body = client.post("/predict/segment", json=vip).json()
    assert body["segment_label"] == "VIP"


def test_get_service_raises_503_without_models() -> None:
    """El path de modelos no cargados devuelve 503 (no 500)."""
    from fastapi import HTTPException

    import api.main as m

    saved = m._state.get("service")
    m._state["service"] = None
    m._state["error"] = "modelos no cargados (test)"
    try:
        with pytest.raises(HTTPException) as exc_info:
            m.get_service()
        assert exc_info.value.status_code == 503
    finally:
        m._state["service"] = saved


def test_predict_churn(client, sample_features) -> None:
    resp = client.post("/predict/churn", json=sample_features)
    assert resp.status_code == 200
    body = resp.json()
    assert 0.0 <= body["churn_probability"] <= 1.0
    assert body["risk_level"] in ("Bajo", "Medio", "Alto")


def test_predict_segment(client, sample_features) -> None:
    resp = client.post("/predict/segment", json=sample_features)
    assert resp.status_code == 200
    assert resp.json()["segment_label"] in VALID_SEGMENTS


def test_predict_combined(client, sample_features) -> None:
    resp = client.post("/predict", json=sample_features)
    assert resp.status_code == 200
    body = resp.json()
    assert body["segment_label"] in VALID_SEGMENTS
    assert "recommendation" in body


def test_predict_minimal_payload(client) -> None:
    resp = client.post("/predict", json={"Recency": 100, "Frequency": 2, "Monetary": 200})
    assert resp.status_code == 200


def test_predict_batch(client, sample_features) -> None:
    payload = {"customers": [sample_features, {"Recency": 300, "Frequency": 1, "Monetary": 50}]}
    resp = client.post("/predict/batch", json=payload)
    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 2


def test_validation_rejects_negative_recency(client) -> None:
    resp = client.post("/predict", json={"Recency": -5, "Frequency": 1, "Monetary": 50})
    assert resp.status_code == 422


def test_validation_requires_mandatory_fields(client) -> None:
    resp = client.post("/predict", json={"Frequency": 1, "Monetary": 50})
    assert resp.status_code == 422
