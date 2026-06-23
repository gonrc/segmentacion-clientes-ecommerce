"""Tests de la capa de servicio (API REST FastAPI)."""

from __future__ import annotations

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
    assert len(resp.json()["required_features"]) == 14


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
