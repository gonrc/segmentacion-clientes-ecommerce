# mypy: ignore-errors
"""Cliente HTTP para consumir la API REST de scoring desde la interfaz Streamlit.

Aísla el detalle de transporte (requests + URL base) para que la app solo hable de
"pedir un score". La URL se toma de la variable de entorno ``API_URL`` (default
``http://localhost:8000``), lo que permite apuntar al contenedor en docker-compose.
"""

from __future__ import annotations

import os
from typing import Any

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
DEFAULT_TIMEOUT = 10
HTTP_ERROR_STATUS = 400


class ApiError(RuntimeError):
    """Error al consumir la API (conexión, timeout o status != 2xx)."""


def health() -> dict[str, Any]:
    try:
        resp = requests.get(f"{API_URL}/health", timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        raise ApiError(f"No se pudo contactar la API en {API_URL}: {exc}") from exc


def score_customer(features: dict[str, float]) -> dict[str, Any]:
    """Llama a POST /predict y devuelve el scoring combinado (segmento + churn)."""
    try:
        resp = requests.post(f"{API_URL}/predict", json=features, timeout=DEFAULT_TIMEOUT)
    except requests.RequestException as exc:
        raise ApiError(f"No se pudo contactar la API en {API_URL}: {exc}") from exc
    if resp.status_code >= HTTP_ERROR_STATUS:
        detail = _safe_detail(resp)
        raise ApiError(f"La API respondió {resp.status_code}: {detail}")
    return resp.json()


def _safe_detail(resp: requests.Response) -> str:
    try:
        return str(resp.json().get("detail", resp.text))
    except ValueError:
        return resp.text
