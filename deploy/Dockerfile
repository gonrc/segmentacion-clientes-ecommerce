# Imagen única para los dos servicios (API y Streamlit): mismas dependencias,
# distinto comando de arranque en docker-compose. Mantiene el entorno alineado y
# evita drift de versiones entre la capa de servicio y la interfaz.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # OpenBLAS/OMP a 1 hilo: evita cuelgues de init de thread-pool en entornos
    # restringidos y hace el arranque del contenedor predecible.
    OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# uv: gestor de dependencias del proyecto (mismo lockfile que en local).
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

# 1) Instalar solo dependencias de runtime (sin grupos dev/docs) desde el lockfile.
#    Se copia primero pyproject+lock para aprovechar la cache de capas de Docker.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-default-groups

# 2) Copiar el código de la aplicación.
COPY src/ ./src/
COPY api/ ./api/
COPY notebooks/7-deploy/ ./notebooks/7-deploy/

# Los artefactos de datos/modelos se montan como volumen en docker-compose
# (no se hornean en la imagen porque viven fuera de git y pueden cambiar).

EXPOSE 8000 8501

# Default: levantar la API. docker-compose sobreescribe el comando del servicio Streamlit.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
