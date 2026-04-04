#!/usr/bin/env python3
"""
Script para ejecutar notebooks de Jupyter programaticamente.
Uso: python execute_notebook.py <ruta_al_notebook>
"""
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path


def execute_notebook(notebook_path):
    """Ejecuta un notebook y guarda el resultado con outputs."""
    notebook_path = Path(notebook_path)

    if not notebook_path.exists():
        print(f"Error: Notebook no encontrado: {notebook_path}")
        sys.exit(1)

    print(f"Ejecutando notebook: {notebook_path}")

    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    try:
        ep.preprocess(nb, {'metadata': {'path': str(notebook_path.parent.resolve())}})
        print(f"✓ Notebook ejecutado exitosamente")
    except Exception as e:
        print(f"✗ Error al ejecutar notebook: {e}")
        sys.exit(1)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"✓ Notebook guardado con outputs: {notebook_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python execute_notebook.py <ruta_al_notebook>")
        sys.exit(1)

    execute_notebook(sys.argv[1])
