# mypy: ignore-errors
from __future__ import annotations

import pickle
import random
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, silhouette_score

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
HIGH_RISK_THRESHOLD = 0.6
MEDIUM_RISK_THRESHOLD = 0.4
DEFAULT_CHURN_THRESHOLD = MEDIUM_RISK_THRESHOLD
DEFAULT_TOP_N = 25
MAX_TOP_N = 200
SEGMENT_NOISE_FRACTION = 0.06
MIN_CLUSTER_FEATURES = 2
MIN_CLUSTER_COUNT = 2
MIN_CLUSTER_ROWS = 10

ARTIFACTS = {
    "clientes_segmentados": DATA_DIR / "07_model_output/clientes_segmentados.parquet",
    "churn_predictions": DATA_DIR / "07_model_output/churn_predictions.parquet",
    "churn_dataset": DATA_DIR / "05_model_input/churn_dataset.parquet",
    "kmeans_model": DATA_DIR / "06_models/kmeans_model.pkl",
    "churn_model": DATA_DIR / "06_models/churn_model.pkl",
}

REPORTS = {
    "segment_dashboard": DATA_DIR / "08_reporting/segment_dashboard.png",
    "churn_by_segment": DATA_DIR / "08_reporting/churn_by_segment.png",
    "segment_churn_risk": DATA_DIR / "08_reporting/segment_churn_risk.png",
    "churn_feature_importance": DATA_DIR / "08_reporting/churn_feature_importance.png",
    "churn_confusion_matrices": DATA_DIR / "08_reporting/churn_confusion_matrices.png",
    "churn_roc_curves": DATA_DIR / "08_reporting/churn_roc_curves.png",
    "clustering_k_selection": DATA_DIR / "08_reporting/clustering_k_selection.png",
    "clustering_heatmap": DATA_DIR / "08_reporting/clustering_heatmap.png",
}

SEGMENT_ACTIONS = {
    "VIP": "Retención prioritaria: contacto personalizado, beneficios por continuidad y alertas de riesgo.",
    "Compradores de Sets": "Promover bundles, packs y cross-selling de productos complementarios.",
    "En Riesgo": "Revisar fricciones, cancelaciones y experiencia post-compra antes de invertir en upselling.",
    "Dormidos": "Campañas de reactivación de bajo costo con ofertas simples y mensajes automatizados.",
}

SEGMENT_DESCRIPTIONS = {
    "VIP": "Clientes de alto valor, alta frecuencia y mayor participación en revenue.",
    "Compradores de Sets": "Clientes con afinidad marcada por productos tipo set o pack.",
    "En Riesgo": "Clientes con mayor cancel rate y bajo revenue relativo.",
    "Dormidos": "Clientes con baja actividad reciente y menor frecuencia de compra.",
}

RISK_LABELS = {
    "Bajo": "Mantener comunicación regular y beneficios livianos.",
    "Medio": "Activar incentivo puntual y monitorear respuesta.",
    "Alto": "Priorizar contacto comercial y acción de retención personalizada.",
}

SIMULATOR_FIELDS = [
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

SIMULATOR_FALLBACKS = {
    "Recency": 90.0,
    "Frequency": 3.0,
    "Monetary": 500.0,
    "Cancel_rate": 0.0,
    "pct_with_color": 0.25,
    "color_diversity": 1.5,
    "is_color_specialist": 0.0,
    "pct_with_material": 0.1,
    "pct_purchases_sets": 0.0,
    "avg_quantity_in_set": 0.0,
    "avg_days_between_purchases": 30.0,
    "months_active": 2.0,
    "n_products_unique": 20.0,
    "avg_order_value": 150.0,
}


def format_money(value: float) -> str:
    return f"£{value:,.0f}"


def format_pct(value: float) -> str:
    return f"{value:.2%}"


def risk_level(probability: float) -> str:
    if probability >= HIGH_RISK_THRESHOLD:
        return "Alto"
    if probability >= MEDIUM_RISK_THRESHOLD:
        return "Medio"
    return "Bajo"


def segment_recommendation(segment: str, probability: float) -> str:
    risk = risk_level(probability)
    segment_action = SEGMENT_ACTIONS.get(
        segment, "Revisar perfil y definir acción comercial puntual."
    )
    return f"Riesgo {risk}. {RISK_LABELS[risk]} {segment_action}"


def require_artifacts() -> None:
    missing = [
        path.relative_to(ROOT)
        for path in [*ARTIFACTS.values(), *REPORTS.values()]
        if not path.exists()
    ]
    if missing:
        st.error("Faltan artefactos necesarios para ejecutar la app.")
        st.write("Archivos faltantes:")
        st.write([str(path) for path in missing])
        st.stop()


@st.cache_data(show_spinner=False)
def load_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


@st.cache_resource(show_spinner=False)
def load_pickle(path: str) -> dict[str, Any]:
    with Path(path).open("rb") as file:
        return pickle.load(file)  # noqa: S301 - trusted model artifacts versioned in this repo.


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    segmented = load_parquet(str(ARTIFACTS["clientes_segmentados"]))
    predictions = load_parquet(str(ARTIFACTS["churn_predictions"]))
    churn_dataset = load_parquet(str(ARTIFACTS["churn_dataset"]))
    return segmented, predictions, churn_dataset


def build_customer_table(segmented: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    pred_cols = [
        "CustomerID",
        "Churn",
        "churn_prob",
        "churn_pred",
        "avg_days_between_purchases",
        "months_active",
        "n_products_unique",
        "avg_order_value",
    ]
    available_pred_cols = [col for col in pred_cols if col in predictions.columns]
    return segmented.merge(predictions[available_pred_cols], on="CustomerID", how="left")


@st.cache_data(show_spinner=False)
def compute_churn_metrics(customer_table: pd.DataFrame) -> dict[str, float]:
    scored = customer_table.dropna(subset=["Churn", "churn_prob"]).copy()
    if scored.empty:
        return {}

    y_true = scored["Churn"].astype(int)
    y_prob = scored["churn_prob"].astype(float)
    y_pred = (
        scored["churn_pred"].astype(int)
        if "churn_pred" in scored.columns
        else (y_prob >= DEFAULT_CHURN_THRESHOLD).astype(int)
    )
    return {
        "auc": float(roc_auc_score(y_true, y_prob)),
        "f1": float(f1_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
    }


@st.cache_data(show_spinner=False)
def compute_cluster_metrics(segmented: pd.DataFrame) -> dict[str, float]:
    cluster_features = [
        "Recency",
        "Frequency",
        "Monetary",
        "Cancel_rate",
        "pct_with_color",
        "color_diversity",
        "pct_with_material",
        "avg_quantity_in_set",
        "pct_purchases_sets",
    ]
    available = [feature for feature in cluster_features if feature in segmented.columns]
    if "Cluster" not in segmented.columns or len(available) < MIN_CLUSTER_FEATURES:
        return {}

    base = segmented.dropna(subset=[*available, "Cluster"]).copy()
    if base["Cluster"].nunique() < MIN_CLUSTER_COUNT or len(base) < MIN_CLUSTER_ROWS:
        return {}

    score = float(silhouette_score(base[available], base["Cluster"].astype(int)))
    return {"silhouette": score}


def cluster_label_map(segmented: pd.DataFrame) -> dict[int, str]:
    labels = (
        segmented.groupby("Cluster")["Segment_label"]
        .agg(lambda values: values.mode().iloc[0])
        .to_dict()
    )
    return {int(cluster): str(label) for cluster, label in labels.items()}


def display_report_image(key: str, caption: str) -> None:
    path = REPORTS[key]
    if path.exists():
        st.image(str(path), caption=caption, width="stretch")
    else:
        st.warning(f"No se encontró {path.relative_to(ROOT)}")


def render_header() -> None:
    st.set_page_config(
        page_title="Segmentación y Churn de Clientes E-commerce",
        page_icon=":bar_chart:",
        layout="wide",
    )
    st.title("Segmentación y Churn de Clientes E-commerce")
    st.caption("Entrega 04 - Prototipo funcional para exploración, scoring y despliegue")


def render_sidebar(customer_table: pd.DataFrame) -> None:
    st.sidebar.header("Contexto")
    st.sidebar.metric("Clientes segmentados", f"{customer_table['CustomerID'].nunique():,}")
    st.sidebar.metric(
        "Clientes con churn score",
        f"{customer_table['churn_prob'].notna().sum():,}",
    )
    st.sidebar.markdown("---")
    st.sidebar.write("Modelos usados:")
    st.sidebar.write("- K-Means para segmentación")
    st.sidebar.write("- Random Forest para churn")


def render_executive_summary(customer_table: pd.DataFrame) -> None:
    scored = customer_table.dropna(subset=["churn_prob"])
    vip_risk = scored[
        (scored["Segment_label"] == "VIP") & (scored["churn_prob"] >= DEFAULT_CHURN_THRESHOLD)
    ]
    risk_clients = scored[scored["churn_prob"] >= DEFAULT_CHURN_THRESHOLD]

    with st.container(border=True):
        st.markdown("#### KPIs de negocio")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Clientes segmentados", f"{customer_table['CustomerID'].nunique():,}")
        col2.metric("Clientes con score", f"{len(scored):,}")
        col3.metric("Churn real promedio", format_pct(float(scored["Churn"].mean())))
        col4.metric("Prob. churn media", format_pct(float(scored["churn_prob"].mean())))
        col5.metric("VIP en riesgo", f"{len(vip_risk):,}")
        st.metric(
            "Revenue en riesgo (probabilidad >= 0,40)",
            format_money(float(risk_clients["Monetary"].sum())),
        )
    with st.container(border=True):
        st.markdown("#### Metodología en una línea")
        st.write(
            "- **Segmentación (K-Means):** identifica perfiles de clientes para orientar estrategias.\n"
            "- **Churn (Random Forest):** estima probabilidad de abandono para priorizar retención."
        )
        st.info(
            "Lectura ejecutiva: la solución combina segmentos de negocio con probabilidad de churn "
            "para priorizar acciones comerciales, especialmente en clientes VIP con riesgo elevado."
        )
        st.caption(
            "Nota: el umbral de priorización actual es 0.40. Puede ajustarse en la pestaña de Churn."
        )
    churn_metrics = compute_churn_metrics(customer_table)
    if churn_metrics:
        with st.container(border=True):
            st.markdown("#### Validación técnica (churn)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("AUC-ROC", f"{churn_metrics['auc']:.3f}")
            m2.metric("F1-score", f"{churn_metrics['f1']:.3f}")
            m3.metric("Precision", f"{churn_metrics['precision']:.3f}")
            m4.metric("Recall", f"{churn_metrics['recall']:.3f}")
            display_report_image("churn_confusion_matrices", "Matriz de confusión (test)")

    display_report_image("segment_dashboard", "Dashboard de segmentos")


def render_segments(customer_table: pd.DataFrame) -> None:
    agg = (
        customer_table.groupby("Segment_label", dropna=False)
        .agg(
            clientes=("CustomerID", "count"),
            revenue=("Monetary", "sum"),
            recency=("Recency", "mean"),
            frequency=("Frequency", "mean"),
            monetary=("Monetary", "mean"),
            cancel_rate=("Cancel_rate", "mean"),
            churn_real=("Churn", "mean"),
            churn_prob=("churn_prob", "mean"),
        )
        .round(3)
        .sort_values("revenue", ascending=False)
    )
    with st.container(border=True):
        st.subheader("Perfil agregado por segmento")
        st.dataframe(agg, width="stretch")
        st.caption(
            "Sugerencia de lectura: priorizar segmentos con mayor revenue y mayor churn_prob promedio."
        )
        cluster_metrics = compute_cluster_metrics(customer_table)
        if cluster_metrics:
            st.metric("Silhouette score (clustering)", f"{cluster_metrics['silhouette']:.3f}")

    with st.container(border=True):
        st.subheader("Interpretación comercial por segmento")
        cols = st.columns(4)
        for col, (segment, description) in zip(cols, SEGMENT_DESCRIPTIONS.items(), strict=False):
            with col:  # noqa: SIM117
                with st.container(border=True):
                    st.markdown(f"**{segment}**")
                    st.write(description)
                    st.caption(SEGMENT_ACTIONS[segment])

    with st.container(border=True):
        st.subheader("Diagnóstico del clustering")
        left, right = st.columns(2)
        with left:
            display_report_image("clustering_heatmap", "Centroides normalizados")
        with right:
            display_report_image("clustering_k_selection", "Selección de k")


def render_churn(customer_table: pd.DataFrame) -> None:
    scored = customer_table.dropna(subset=["churn_prob"]).copy()
    segments = ["Todos", *sorted(scored["Segment_label"].dropna().unique().tolist())]

    col1, col2, col3 = st.columns([2, 2, 1])
    selected_segment = col1.selectbox("Segmento", segments)
    threshold = col2.slider(
        "Umbral mínimo de probabilidad",
        0.0,
        1.0,
        DEFAULT_CHURN_THRESHOLD,
        0.05,
    )
    top_n = col3.number_input(
        "Top N",
        min_value=5,
        max_value=MAX_TOP_N,
        value=DEFAULT_TOP_N,
        step=5,
    )

    filtered = scored[scored["churn_prob"] >= threshold]
    if selected_segment != "Todos":
        filtered = filtered[filtered["Segment_label"] == selected_segment]

    ranking_cols = [
        "CustomerID",
        "Segment_label",
        "churn_prob",
        "churn_pred",
        "Monetary",
        "Recency",
        "Frequency",
    ]
    ranking = filtered.sort_values("churn_prob", ascending=False)[ranking_cols].head(int(top_n))

    with st.container(border=True):
        st.subheader("Ranking de clientes en riesgo")
        st.dataframe(ranking, width="stretch", hide_index=True)
        st.caption(
            "`churn_prob` es probabilidad estimada; `churn_pred` es la clase final según el umbral del modelo."
        )
        st.caption(
            "Uso recomendado: ranking para priorización comercial, no como explicación causal."
        )

    with st.container(border=True):
        st.subheader("Visuales de churn para negocio")
        left, right = st.columns(2)
        with left:
            display_report_image("churn_feature_importance", "Importancia de variables")
        with right:
            display_report_image("churn_by_segment", "Churn por segmento")
    with st.expander("Ver métricas técnicas de validación (detalle)"):
        c1, c2 = st.columns(2)
        with c1:
            display_report_image("churn_confusion_matrices", "Matrices de confusión")
        with c2:
            display_report_image("churn_roc_curves", "Curvas ROC")


def render_customer_lookup(customer_table: pd.DataFrame) -> None:
    scored = customer_table.dropna(subset=["churn_prob"]).copy()
    customer_ids = sorted(scored["CustomerID"].astype(int).tolist())
    selected_id = st.selectbox("CustomerID", customer_ids)
    row = scored[scored["CustomerID"] == selected_id].iloc[0]
    probability = float(row["churn_prob"])
    segment = str(row["Segment_label"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Segmento", segment)
    col2.metric("Probabilidad churn", format_pct(probability))
    col3.metric("Predicción", "Churn" if int(row["churn_pred"]) == 1 else "Retenido")
    col4.metric("Monetary", format_money(float(row["Monetary"])))

    st.subheader("Perfil del cliente")

    def customer_value(column: str, fmt: str = "float") -> str:  # noqa: PLR0911
        if column not in row.index:
            return "-"
        value = row[column]
        if pd.isna(value):
            return "-"
        if fmt == "pct":
            return format_pct(float(value))
        if fmt == "money":
            return format_money(float(value))
        if fmt == "int":
            return f"{int(float(value)):,}"
        if fmt == "float":
            return f"{float(value):.2f}"
        return str(value)

    c1, c2, c3 = st.columns(3)
    with c1:  # noqa: SIM117
        with st.container(border=True):
            st.markdown("#### RFM y valor")
            rfm_df = pd.DataFrame(
                [
                    ("Recency (días)", customer_value("Recency", "int")),
                    ("Frequency", customer_value("Frequency", "int")),
                    ("Monetary", customer_value("Monetary", "money")),
                    ("Cancel rate", customer_value("Cancel_rate", "pct")),
                    ("Ticket promedio", customer_value("avg_order_value", "money")),
                ],
                columns=["Métrica", "Valor"],
            )
            st.dataframe(rfm_df, width="stretch", hide_index=True)

    with c2:  # noqa: SIM117
        with st.container(border=True):
            st.markdown("#### Afinidad de producto")
            product_df = pd.DataFrame(
                [
                    ("Color dominante", customer_value("dominant_color", "text")),
                    ("% compras con color", customer_value("pct_with_color", "pct")),
                    ("Diversidad de color", customer_value("color_diversity", "float")),
                    ("Material dominante", customer_value("dominant_material", "text")),
                    ("% compras con material", customer_value("pct_with_material", "pct")),
                    ("% compras en sets", customer_value("pct_purchases_sets", "pct")),
                    ("Cantidad promedio en set", customer_value("avg_quantity_in_set", "float")),
                ],
                columns=["Métrica", "Valor"],
            )
            st.dataframe(product_df, width="stretch", hide_index=True)

    with c3:  # noqa: SIM117
        with st.container(border=True):
            st.markdown("#### Actividad y recurrencia")
            activity_df = pd.DataFrame(
                [
                    (
                        "Días promedio entre compras",
                        customer_value("avg_days_between_purchases", "float"),
                    ),
                    ("Meses activos", customer_value("months_active", "float")),
                    ("Productos únicos", customer_value("n_products_unique", "int")),
                ],
                columns=["Métrica", "Valor"],
            )
            st.dataframe(activity_df, width="stretch", hide_index=True)

    st.success(segment_recommendation(segment, probability))


def simulator_key(field: str) -> str:
    return f"simulator_{field}"


def numeric_field_values(field: str, datasets: list[pd.DataFrame]) -> pd.Series:
    values = [
        pd.to_numeric(dataset[field], errors="coerce").dropna()
        for dataset in datasets
        if field in dataset.columns
    ]
    if not values:
        return pd.Series(dtype="float64")
    return pd.concat(values, ignore_index=True)


def simulator_stats(datasets: list[pd.DataFrame]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for field in SIMULATOR_FIELDS:
        values = numeric_field_values(field, datasets)
        fallback = SIMULATOR_FALLBACKS[field]
        if values.empty:
            stats[field] = {"min": fallback, "max": fallback, "median": fallback}
            continue
        stats[field] = {
            "min": float(values.min()),
            "max": float(values.max()),
            "median": float(values.median()),
        }
    return stats


def clamp(value: float, min_value: float, max_value: float) -> float:
    return min(max(value, min_value), max_value)


def initialize_simulator_state(stats: dict[str, dict[str, float]]) -> None:
    for field in SIMULATOR_FIELDS:
        key = simulator_key(field)
        min_value = stats[field]["min"]
        max_value = stats[field]["max"]
        if field == "is_color_specialist":
            st.session_state[key] = bool(st.session_state.get(key, stats[field]["median"]))
            continue
        current_value = float(st.session_state.get(key, stats[field]["median"]))
        st.session_state[key] = clamp(current_value, min_value, max_value)


def build_anchor_pool(churn_dataset: pd.DataFrame, segmented: pd.DataFrame) -> pd.DataFrame:
    churn_cols = [
        "CustomerID",
        *[field for field in SIMULATOR_FIELDS if field in churn_dataset.columns],
    ]
    pool = churn_dataset[churn_cols].copy()

    missing_fields = [field for field in SIMULATOR_FIELDS if field not in pool.columns]
    if missing_fields and "CustomerID" in segmented.columns:
        seg_cols = [
            "CustomerID",
            *[field for field in missing_fields if field in segmented.columns],
        ]
        pool = pool.merge(segmented[seg_cols], on="CustomerID", how="left")

    if "CustomerID" in pool.columns and {"CustomerID", "Segment_label"}.issubset(segmented.columns):
        pool = pool.merge(segmented[["CustomerID", "Segment_label"]], on="CustomerID", how="left")
    else:
        pool["Segment_label"] = "unknown"

    available_fields = [field for field in SIMULATOR_FIELDS if field in pool.columns]
    if not available_fields:
        return pd.DataFrame(columns=[*SIMULATOR_FIELDS, "Segment_label"])

    return pool[[*available_fields, "Segment_label"]]


def segment_sampling_weights(anchor_pool: pd.DataFrame) -> dict[str, float]:
    if anchor_pool.empty or "Segment_label" not in anchor_pool.columns:
        return {}

    weights = (
        anchor_pool["Segment_label"].dropna().astype(str).value_counts(normalize=True).to_dict()
    )
    return {segment: float(weight) for segment, weight in weights.items()}


def real_segment_weights(segmented: pd.DataFrame, anchor_pool: pd.DataFrame) -> dict[str, float]:
    """Pesos de muestreo del target segun la distribucion real de segmentos.

    Se usa la distribucion de `clientes_segmentados` (universo completo) en lugar de
    la del anchor pool (churn_dataset, poblacion filtrada que sobre-representa VIP).
    Se restringe a los segmentos que tienen anchors disponibles y se renormaliza.
    """
    real_weights = segment_sampling_weights(segmented)
    if anchor_pool.empty or "Segment_label" not in anchor_pool.columns:
        return real_weights
    available = set(anchor_pool["Segment_label"].dropna().astype(str).unique())
    filtered = {segment: weight for segment, weight in real_weights.items() if segment in available}
    total = sum(filtered.values())
    if total <= 0:
        return segment_sampling_weights(anchor_pool)
    return {segment: weight / total for segment, weight in filtered.items()}


def randomize_simulator_state(  # noqa: C901, PLR0912
    stats: dict[str, dict[str, float]],
    anchor_pool: pd.DataFrame,
    kmeans_bundle: dict[str, Any],
    labels: dict[int, str],
    sampling_weights: dict[str, float] | None = None,
) -> None:
    if anchor_pool.empty:
        values = {field: float(stats[field]["median"]) for field in SIMULATOR_FIELDS}
        for field in SIMULATOR_FIELDS:
            st.session_state[simulator_key(field)] = (
                bool(round(values[field])) if field == "is_color_specialist" else values[field]
            )
        return

    weights = sampling_weights or segment_sampling_weights(anchor_pool)
    segments = list(weights.keys())
    if segments:
        target_segment = random.choices(  # noqa: S311
            segments, weights=[weights[segment] for segment in segments], k=1
        )[0]
        segment_pool = anchor_pool[anchor_pool["Segment_label"].astype(str) == target_segment]
        if segment_pool.empty:
            segment_pool = anchor_pool
    else:
        target_segment = "VIP"
        segment_pool = anchor_pool

    generated_values: dict[str, float] = {}
    for _ in range(12):
        anchor = segment_pool.sample(n=1).iloc[0]
        candidate_values: dict[str, float] = {}

        for field in SIMULATOR_FIELDS:
            min_value = stats[field]["min"]
            max_value = stats[field]["max"]

            raw_value = anchor.get(field, stats[field]["median"])
            if pd.isna(raw_value):
                raw_value = stats[field]["median"]
            if field == "is_color_specialist":
                candidate_values[field] = float(round(float(raw_value)))
                continue

            base_value = float(raw_value)
            if min_value == max_value:
                candidate_values[field] = float(min_value)
                continue

            if field in segment_pool.columns:
                local_series = pd.to_numeric(segment_pool[field], errors="coerce").dropna()
            else:
                local_series = pd.Series(dtype="float64")

            if local_series.empty:
                local_min = min_value
                local_max = max_value
                local_span = max_value - min_value
            else:
                local_min = float(local_series.quantile(0.05))
                local_max = float(local_series.quantile(0.95))
                local_span = max(local_max - local_min, 1e-6)

            noise_std = max(local_span * SEGMENT_NOISE_FRACTION, abs(base_value) * 0.01, 1e-6)
            candidate = base_value + random.gauss(0, noise_std)
            candidate_values[field] = clamp(
                candidate, max(min_value, local_min), min(max_value, local_max)
            )

        generated_values = candidate_values
        predicted_segment = predict_segment(kmeans_bundle, generated_values, labels)
        if predicted_segment == target_segment:
            break

    for field in SIMULATOR_FIELDS:
        st.session_state[simulator_key(field)] = (
            bool(round(generated_values[field]))
            if field == "is_color_specialist"
            else float(generated_values[field])
        )


def number_input_for_field(field: str, stats: dict[str, dict[str, float]]) -> float:
    min_value = stats[field]["min"]
    max_value = stats[field]["max"]
    if min_value == max_value:
        st.caption(f"{field}: valor fijo observado = {min_value:.4g}")
        return float(
            st.number_input(
                field,
                min_value=min_value,
                max_value=max_value + 1.0,
                key=simulator_key(field),
            )
        )
    return float(
        st.number_input(
            field,
            min_value=min_value,
            max_value=max_value,
            key=simulator_key(field),
        )
    )


def collect_simulation_inputs(
    churn_dataset: pd.DataFrame,
    segmented: pd.DataFrame,
    kmeans_bundle: dict[str, Any],
    labels: dict[int, str],
) -> dict[str, float]:
    stats = simulator_stats([churn_dataset, segmented])
    anchor_pool = build_anchor_pool(churn_dataset, segmented)
    target_weights = real_segment_weights(segmented, anchor_pool)
    initialize_simulator_state(stats)

    st.write("Cargar valores del cliente a evaluar.")
    st.caption(
        "El cliente random parte de un cliente real y aplica una variación pequeña por variable."
    )
    st.caption(
        "Flujo recomendado: 1) generar cliente random, 2) ajustar variables, 3) calcular score."
    )
    if st.button("Generar cliente random", type="secondary"):
        randomize_simulator_state(stats, anchor_pool, kmeans_bundle, labels, target_weights)

    values: dict[str, float] = {}
    s1, s2, s3 = st.columns(3)
    with s1:  # noqa: SIM117
        with st.container(border=True):
            st.markdown("#### RFM y valor")
            values["Recency"] = number_input_for_field("Recency", stats)
            values["Frequency"] = number_input_for_field("Frequency", stats)
            values["Monetary"] = number_input_for_field("Monetary", stats)
            values["Cancel_rate"] = number_input_for_field("Cancel_rate", stats)
            values["avg_order_value"] = number_input_for_field("avg_order_value", stats)

    with s2:  # noqa: SIM117
        with st.container(border=True):
            st.markdown("#### Afinidad de producto")
            values["pct_with_color"] = number_input_for_field("pct_with_color", stats)
            values["color_diversity"] = number_input_for_field("color_diversity", stats)
            values["is_color_specialist"] = float(
                st.checkbox("is_color_specialist", key=simulator_key("is_color_specialist"))
            )
            values["pct_with_material"] = number_input_for_field("pct_with_material", stats)
            values["pct_purchases_sets"] = number_input_for_field("pct_purchases_sets", stats)
            values["avg_quantity_in_set"] = number_input_for_field("avg_quantity_in_set", stats)

    with s3:  # noqa: SIM117
        with st.container(border=True):
            st.markdown("#### Actividad y recurrencia")
            values["avg_days_between_purchases"] = number_input_for_field(
                "avg_days_between_purchases", stats
            )
            values["months_active"] = number_input_for_field("months_active", stats)
            values["n_products_unique"] = number_input_for_field("n_products_unique", stats)
    return values


def predict_probability(bundle: dict[str, Any], values: dict[str, float]) -> float:
    features = list(bundle["features"])
    model_input = pd.DataFrame([{feature: values.get(feature, 0.0) for feature in features}])
    scaler_input = (
        model_input if hasattr(bundle["scaler"], "feature_names_in_") else model_input.to_numpy()
    )
    transformed = bundle["scaler"].transform(scaler_input)
    return float(bundle["model"].predict_proba(transformed)[0, 1])


def predict_segment(
    bundle: dict[str, Any],
    values: dict[str, float],
    labels: dict[int, str],
) -> str:
    features = list(bundle["features"])
    model_input = pd.DataFrame([{feature: values.get(feature, 0.0) for feature in features}])
    scaler_input = (
        model_input if hasattr(bundle["scaler"], "feature_names_in_") else model_input.to_numpy()
    )
    transformed = bundle["scaler"].transform(scaler_input)
    cluster = int(bundle["model"].predict(transformed)[0])
    return labels.get(cluster, f"Cluster {cluster}")


def render_simulator(churn_dataset: pd.DataFrame, segmented: pd.DataFrame) -> None:
    churn_bundle = load_pickle(str(ARTIFACTS["churn_model"]))
    kmeans_bundle = load_pickle(str(ARTIFACTS["kmeans_model"]))
    labels = cluster_label_map(segmented)

    with st.container(border=True):
        values = collect_simulation_inputs(churn_dataset, segmented, kmeans_bundle, labels)

    with st.container(border=True):
        if st.button("Calcular score", type="primary"):
            probability = predict_probability(churn_bundle, values)
            segment = predict_segment(kmeans_bundle, values, labels)
            risk = risk_level(probability)

            col1, col2, col3 = st.columns(3)
            col1.metric("Probabilidad de churn", format_pct(probability))
            col2.metric("Nivel de riesgo", risk)
            col3.metric("Segmento estimado", segment)
            st.success(segment_recommendation(segment, probability))


def render_deployment() -> None:
    with st.container(border=True):
        st.subheader("Arquitectura propuesta")
        st.write(
            "La solución puede operar como un proceso batch semanal o mensual: ingesta de nuevas "
            "transacciones, limpieza, generación de features, scoring de modelos y publicación en "
            "dashboard interno o CRM."
        )
        st.caption("Estado actual: MVP local funcional con Streamlit y artefactos precalculados.")

    with st.container(border=True):
        st.subheader("Recursos requeridos")
        st.write(
            "- Base transaccional actualizada.\n"
            "- Ambiente Python con pandas, scikit-learn y Streamlit.\n"
            "- Almacenamiento de features, predicciones y logs.\n"
            "- Responsable de monitoreo de calidad de datos y performance."
        )

    with st.container(border=True):
        st.subheader("Alternativas para escalar")
        st.table(
            pd.DataFrame(
                [
                    ("MVP", "Streamlit con artefactos precalculados."),
                    ("Equipo comercial", "App interna con refresh batch y datos en base central."),
                    ("Producción", "API de scoring, orquestador y dashboard conectado a CRM."),
                    (
                        "Escala mayor",
                        "Feature store, versionado de modelos y retraining programado.",
                    ),
                ],
                columns=["Nivel", "Alternativa"],
            )
        )

    with st.container(border=True):
        st.subheader("Monitoreo")
        st.write(
            "Monitorear drift de features, cambios en tamaños de segmentos, F1/AUC mensual, "
            "churn real posterior y retorno comercial de acciones de retención."
        )


def main() -> None:
    render_header()
    require_artifacts()
    segmented, predictions, churn_dataset = load_data()
    customer_table = build_customer_table(segmented, predictions)
    render_sidebar(customer_table)

    tabs = st.tabs(
        [
            "Resumen ejecutivo",
            "Segmentos",
            "Churn",
            "Buscador de cliente",
            "Simulador",
            "Despliegue",
        ]
    )
    with tabs[0]:
        render_executive_summary(customer_table)
    with tabs[1]:
        render_segments(customer_table)
    with tabs[2]:
        render_churn(customer_table)
    with tabs[3]:
        render_customer_lookup(customer_table)
    with tabs[4]:
        render_simulator(churn_dataset, segmented)
    with tabs[5]:
        render_deployment()


if __name__ == "__main__":
    main()
