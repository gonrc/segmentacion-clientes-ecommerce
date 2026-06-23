"""Esquemas Pydantic: definen las **entradas y salidas** de la API de forma explícita.

Pydantic valida tipos y rangos automáticamente; FastAPI los usa para generar la
documentación OpenAPI/Swagger en ``/docs``.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CustomerFeatures(BaseModel):
    """Features de un cliente a evaluar.

    Solo ``Recency``, ``Frequency`` y ``Monetary`` son obligatorias; el resto tiene
    default 0.0 para aceptar payloads parciales. Cada modelo toma internamente el
    subconjunto de features que necesita.
    """

    Recency: float = Field(..., ge=0, description="Días desde la última compra.")
    Frequency: float = Field(..., ge=0, description="Cantidad de compras (facturas).")
    Monetary: float = Field(..., ge=0, description="Revenue neto acumulado del cliente.")
    Cancel_rate: float = Field(
        0.0, ge=0, description="Tasa de cancelación en % (revenue cancelado / bruto x 100)."
    )
    pct_with_color: float = Field(
        0.0, ge=0, description="% de compras con color detectado (escala 0-100)."
    )
    color_diversity: float = Field(
        0.0, ge=0, description="Cantidad de colores distintos comprados."
    )
    is_color_specialist: float = Field(
        0.0, ge=0, le=1, description="1 si concentra sus compras en un color, 0 si no."
    )
    pct_with_material: float = Field(
        0.0, ge=0, description="% de compras con material detectado (escala 0-100)."
    )
    pct_purchases_sets: float = Field(
        0.0, ge=0, description="% de compras que son sets/packs (escala 0-100)."
    )
    avg_quantity_in_set: float = Field(0.0, ge=0, description="Cantidad promedio de ítems por set.")
    avg_days_between_purchases: float = Field(0.0, ge=0, description="Días promedio entre compras.")
    months_active: float = Field(0.0, ge=0, description="Meses con actividad de compra.")
    n_products_unique: float = Field(
        0.0, ge=0, description="Cantidad de productos únicos comprados."
    )
    avg_order_value: float = Field(0.0, ge=0, description="Ticket promedio por compra.")

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }


class ChurnResponse(BaseModel):
    churn_probability: float = Field(..., description="Probabilidad estimada de churn (0-1).")
    churn_prediction: int = Field(
        ..., description="Clase predicha por el modelo (0=retiene, 1=churn)."
    )
    risk_level: str = Field(..., description="Nivel de riesgo de negocio: Bajo, Medio o Alto.")


class SegmentResponse(BaseModel):
    cluster: int = Field(..., description="Índice del cluster asignado por K-Means.")
    segment_label: str = Field(..., description="Etiqueta de negocio del segmento.")
    segment_description: str = Field(..., description="Descripción del segmento.")


class ScoreResponse(SegmentResponse, ChurnResponse):
    """Respuesta combinada: segmento + churn + recomendación accionable."""

    recommendation: str = Field(..., description="Acción comercial sugerida.")


class BatchScoreRequest(BaseModel):
    customers: list[CustomerFeatures] = Field(..., min_length=1, max_length=5000)


class BatchScoreResponse(BaseModel):
    results: list[ScoreResponse]


class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    detail: str | None = None


class ErrorResponse(BaseModel):
    detail: str
