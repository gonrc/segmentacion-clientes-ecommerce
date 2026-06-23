"""Lógica de modelo para la segmentación de clientes y la predicción de churn.

Esta es la **capa de lógica de modelo**, deliberadamente separada de la capa de
servicio (la API en `api/`). No conoce nada de HTTP ni de FastAPI: solo carga los
artefactos serializados en la Entrega 03 y expone métodos de inferencia puros sobre
diccionarios de features. Tanto la API REST como cualquier otro consumidor (tests,
notebooks, jobs batch) pueden importar esta clase y reutilizarla.

Artefactos consumidos (generados en la Entrega 03):
- ``data/06_models/kmeans_model.pkl``  -> bundle {model, scaler, features}
- ``data/06_models/churn_model.pkl``   -> bundle {model, scaler, features, model_name}
- ``data/06_models/cluster_labels.json`` -> mapeo cluster (int) -> etiqueta de negocio
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

import pandas as pd

# Raíz del repo: .../src/inference/model_service.py -> parents[2]
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODELS_DIR = ROOT / "data" / "06_models"

# Umbrales de negocio para traducir la probabilidad de churn a un nivel de riesgo.
HIGH_RISK_THRESHOLD = 0.6
MEDIUM_RISK_THRESHOLD = 0.4

# Contrato de entrada: unión de las features que requieren ambos modelos.
# Cada modelo selecciona internamente el subconjunto que necesita desde su bundle.
ALL_FEATURES: list[str] = [
    "Recency",
    "Frequency",
    "Monetary",
    "Cancel_rate",
    "pct_with_color",
    "color_diversity",
    "is_color_specialist",
    "pct_with_material",
    "pct_purchases_sets",
    "avg_quantity_in_set",
    "avg_days_between_purchases",
    "months_active",
    "n_products_unique",
    "avg_order_value",
]

SEGMENT_DESCRIPTIONS = {
    "VIP": "Clientes de alto valor, alta frecuencia y mayor participación en revenue.",
    "Compradores de Sets": "Clientes con afinidad marcada por productos tipo set o pack.",
    "En Riesgo": "Clientes con mayor cancel rate y bajo revenue relativo.",
    "Dormidos": "Clientes con baja actividad reciente y menor frecuencia de compra.",
}

SEGMENT_ACTIONS = {
    "VIP": "Retención prioritaria: contacto personalizado, beneficios por continuidad y alertas de riesgo.",
    "Compradores de Sets": "Promover bundles, packs y cross-selling de productos complementarios.",
    "En Riesgo": "Revisar fricciones, cancelaciones y experiencia post-compra antes de invertir en upselling.",
    "Dormidos": "Campañas de reactivación de bajo costo con ofertas simples y mensajes automatizados.",
}

RISK_LABELS = {
    "Bajo": "Mantener comunicación regular y beneficios livianos.",
    "Medio": "Activar incentivo puntual y monitorear respuesta.",
    "Alto": "Priorizar contacto comercial y acción de retención personalizada.",
}


class ModelNotLoadedError(RuntimeError):
    """Se levanta cuando faltan artefactos o no se pudieron cargar los modelos."""


def risk_level(probability: float) -> str:
    if probability >= HIGH_RISK_THRESHOLD:
        return "Alto"
    if probability >= MEDIUM_RISK_THRESHOLD:
        return "Medio"
    return "Bajo"


def recommendation(segment: str, probability: float) -> str:
    risk = risk_level(probability)
    action = SEGMENT_ACTIONS.get(segment, "Revisar perfil y definir acción comercial puntual.")
    return f"Riesgo {risk}. {RISK_LABELS[risk]} {action}"


class ModelService:
    """Encapsula la carga de los modelos serializados y la inferencia.

    Diseñada para instanciarse una sola vez (singleton a nivel de proceso) y reusarse
    en cada request. La carga es perezosa: ocurre en ``__init__`` y, si falta algún
    artefacto, levanta :class:`ModelNotLoadedError` con un mensaje claro.
    """

    def __init__(self, models_dir: str | Path | None = None) -> None:
        self.models_dir = Path(models_dir) if models_dir else DEFAULT_MODELS_DIR
        self._kmeans: dict[str, Any] = {}
        self._churn: dict[str, Any] = {}
        self._cluster_labels: dict[int, str] = {}
        self._load()

    # ------------------------------------------------------------------ carga
    def _load(self) -> None:
        kmeans_path = self.models_dir / "kmeans_model.pkl"
        churn_path = self.models_dir / "churn_model.pkl"
        labels_path = self.models_dir / "cluster_labels.json"

        missing = [p for p in (kmeans_path, churn_path, labels_path) if not p.exists()]
        if missing:
            names = ", ".join(str(p) for p in missing)
            raise ModelNotLoadedError(f"Faltan artefactos de modelo: {names}")

        try:
            with kmeans_path.open("rb") as fh:
                self._kmeans = pickle.load(fh)  # noqa: S301 - artefactos propios versionados
            with churn_path.open("rb") as fh:
                self._churn = pickle.load(fh)  # noqa: S301 - artefactos propios versionados
            with labels_path.open(encoding="utf-8") as fh:
                raw_labels = json.load(fh)
        except Exception as exc:
            raise ModelNotLoadedError(f"No se pudieron cargar los modelos: {exc}") from exc

        self._cluster_labels = {int(k): str(v) for k, v in raw_labels.items()}

    # --------------------------------------------------------------- metadata
    @property
    def churn_features(self) -> list[str]:
        return list(self._churn["features"])

    @property
    def segment_features(self) -> list[str]:
        return list(self._kmeans["features"])

    @property
    def required_features(self) -> list[str]:
        return list(ALL_FEATURES)

    @property
    def segments(self) -> dict[str, str]:
        return dict(SEGMENT_DESCRIPTIONS)

    def metadata(self) -> dict[str, Any]:
        return {
            "required_features": self.required_features,
            "churn_features": self.churn_features,
            "segment_features": self.segment_features,
            "segments": [
                {"label": label, "description": desc}
                for label, desc in SEGMENT_DESCRIPTIONS.items()
            ],
            "risk_thresholds": {
                "medium": MEDIUM_RISK_THRESHOLD,
                "high": HIGH_RISK_THRESHOLD,
            },
            "churn_model": self._churn.get("model_name", type(self._churn["model"]).__name__),
            "segment_model": type(self._kmeans["model"]).__name__,
        }

    # -------------------------------------------------------------- inferencia
    @staticmethod
    def _build_matrix(features: dict[str, float], feature_order: list[str], scaler: Any) -> Any:
        """Arma la matriz de entrada respetando el orden de features del modelo.

        El scaler del K-Means es un ``Pipeline`` entrenado con nombres de columna
        (``feature_names_in_``) y espera un DataFrame; el del churn es un
        ``StandardScaler`` sin nombres y espera un array. Replicamos esa distinción.
        """
        frame = pd.DataFrame([{name: float(features.get(name, 0.0)) for name in feature_order}])
        scaler_input = frame if hasattr(scaler, "feature_names_in_") else frame.to_numpy()
        return scaler.transform(scaler_input)

    def predict_churn(self, features: dict[str, float]) -> dict[str, Any]:
        scaler = self._churn["scaler"]
        model = self._churn["model"]
        matrix = self._build_matrix(features, self.churn_features, scaler)
        probability = float(model.predict_proba(matrix)[0, 1])
        prediction = int(model.predict(matrix)[0])
        return {
            "churn_probability": probability,
            "churn_prediction": prediction,
            "risk_level": risk_level(probability),
        }

    def predict_segment(self, features: dict[str, float]) -> dict[str, Any]:
        scaler = self._kmeans["scaler"]
        model = self._kmeans["model"]
        matrix = self._build_matrix(features, self.segment_features, scaler)
        cluster = int(model.predict(matrix)[0])
        label = self._cluster_labels.get(cluster, f"Cluster {cluster}")
        return {
            "cluster": cluster,
            "segment_label": label,
            "segment_description": SEGMENT_DESCRIPTIONS.get(label, ""),
        }

    def score_customer(self, features: dict[str, float]) -> dict[str, Any]:
        """Scoring combinado: segmento + churn + recomendación de negocio."""
        churn = self.predict_churn(features)
        segment = self.predict_segment(features)
        return {
            **segment,
            **churn,
            "recommendation": recommendation(segment["segment_label"], churn["churn_probability"]),
        }
