"""Genera ``data/06_models/feature_stats.json`` con estadísticas por feature.

Para cada feature del contrato de la API se calcula min, max y mediana sobre los
datos de entrenamiento. La capa de servicio los usa para:
- imputar features ausentes con la mediana (en vez de 0, que distorsiona el segmento),
- exponer rangos esperados en ``/metadata``,
- validar entradas con cotas razonables.

Se prefiere ``rfm_clientes_enriched`` (base completa de 4.338 clientes) y se completa
con ``churn_dataset`` para las features de actividad que solo viven ahí.

Uso (desde la raíz del repo):
    uv run python deploy/build_feature_stats.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RFM = ROOT / "data" / "04_feature" / "rfm_clientes_enriched.parquet"
CHURN = ROOT / "data" / "05_model_input" / "churn_dataset.parquet"
OUTPUT = ROOT / "data" / "06_models" / "feature_stats.json"

FEATURES = [
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


def main() -> None:
    frames = []
    for path in (RFM, CHURN):
        if path.exists():
            frames.append(pd.read_parquet(path))
    if not frames:
        raise SystemExit(
            "No se encontraron los datasets de entrenamiento. Generá la Entrega 02/03."
        )

    stats: dict[str, dict[str, float]] = {}
    for feature in FEATURES:
        series = None
        for frame in frames:
            if feature in frame.columns:
                series = pd.to_numeric(frame[feature], errors="coerce").dropna()
                break
        if series is None or series.empty:
            continue
        stats[feature] = {
            "min": float(series.min()),
            "max": float(series.max()),
            "median": float(series.median()),
        }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2, ensure_ascii=False)
    print(f"Escrito {OUTPUT.relative_to(ROOT)} con {len(stats)} features.")
    for feat, st in stats.items():
        print(f"  {feat:26s} min={st['min']:.3g}  median={st['median']:.3g}  max={st['max']:.3g}")


if __name__ == "__main__":
    main()
