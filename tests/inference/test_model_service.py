"""Tests de la capa de lógica de modelo (``ModelService``)."""

from __future__ import annotations

import pytest

from tests.conftest import requires_models

pytestmark = requires_models

VALID_SEGMENTS = {"VIP", "Compradores de Sets", "En Riesgo", "Dormidos"}


def test_metadata_lists_features_and_models(service) -> None:
    md = service.metadata()
    assert len(md["required_features"]) == 14
    assert md["segment_model"] == "KMeans"
    assert md["churn_model"]
    assert {s["label"] for s in md["segments"]} == VALID_SEGMENTS


def test_predict_churn_returns_probability_and_risk(service, sample_features) -> None:
    result = service.predict_churn(sample_features)
    assert 0.0 <= result["churn_probability"] <= 1.0
    assert result["churn_prediction"] in (0, 1)
    assert result["risk_level"] in ("Bajo", "Medio", "Alto")


def test_predict_segment_returns_known_label(service, sample_features) -> None:
    result = service.predict_segment(sample_features)
    assert result["segment_label"] in VALID_SEGMENTS
    assert isinstance(result["cluster"], int)


def test_score_customer_combines_outputs(service, sample_features) -> None:
    result = service.score_customer(sample_features)
    assert result["segment_label"] in VALID_SEGMENTS
    assert 0.0 <= result["churn_probability"] <= 1.0
    assert result["recommendation"]


def test_dormant_customer_is_higher_risk_than_active(service, sample_features) -> None:
    """Un cliente inactivo debería tener mayor probabilidad de churn que un VIP activo."""
    dormant = {"Recency": 300, "Frequency": 1, "Monetary": 50.0}
    active = service.predict_churn(sample_features)["churn_probability"]
    inactive = service.predict_churn(dormant)["churn_probability"]
    assert inactive > active


def test_missing_features_default_to_zero(service) -> None:
    """El servicio acepta payloads parciales (features ausentes -> 0.0)."""
    result = service.score_customer({"Recency": 100, "Frequency": 2, "Monetary": 200.0})
    assert result["segment_label"] in VALID_SEGMENTS


def test_missing_artifacts_raises() -> None:
    from src.inference.model_service import ModelNotLoadedError, ModelService

    with pytest.raises(ModelNotLoadedError):
        ModelService(models_dir="/tmp/no_existe_dir_modelos_xyz")
