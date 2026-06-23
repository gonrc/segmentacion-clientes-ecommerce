"""Genera ``data/06_models/cluster_labels.json`` a partir de los clientes segmentados.

La API necesita un mapeo cluster (int) -> etiqueta de negocio para traducir la salida
del K-Means. Ese mapeo se deriva de ``clientes_segmentados.parquet`` (salida de la
Entrega 03): la etiqueta de cada cluster es la moda de ``Segment_label`` entre sus
clientes. Este script reproduce ese artefacto sin reentrenar el modelo.

Uso (desde la raíz del repo):
    uv run python deploy/build_cluster_labels.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEGMENTED = ROOT / "data" / "07_model_output" / "clientes_segmentados.parquet"
OUTPUT = ROOT / "data" / "06_models" / "cluster_labels.json"


def build_label_map(segmented: pd.DataFrame) -> dict[int, str]:
    labels = (
        segmented.groupby("Cluster")["Segment_label"]
        .agg(lambda values: values.mode().iloc[0])
        .to_dict()
    )
    return {int(cluster): str(label) for cluster, label in labels.items()}


def main() -> None:
    if not SEGMENTED.exists():
        raise SystemExit(
            f"No se encontró {SEGMENTED}. Generá primero los artefactos de la Entrega 03."
        )
    segmented = pd.read_parquet(SEGMENTED)
    label_map = build_label_map(segmented)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as fh:
        json.dump(label_map, fh, indent=2, ensure_ascii=False)
    print(f"Escrito {OUTPUT.relative_to(ROOT)}: {label_map}")


if __name__ == "__main__":
    main()
