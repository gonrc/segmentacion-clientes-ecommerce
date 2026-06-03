# Checklist de Cumplimiento - Entrega 03

**Proyecto:** Segmentacion de clientes y analisis comercial en e-commerce  
**Materia:** Ciencia de Datos Aplicada - ITBA  
**Grupo:** Grupo 12  
**Fecha de revision:** 2026-06-03  

Este documento cruza la consigna de la Entrega 03 contra los artefactos actuales del proyecto.

## Resumen Ejecutivo

| Componente | Estado | Comentario |
|---|---|---|
| Entrenamiento y validacion del modelo | Cubierto | Hay clustering, churn, metricas y analisis de resultados. |
| Reflexion critica | Cubierto | Incluida en el notebook de interpretacion y consolidada en el notebook final. |
| Prototipo funcional | Cubierto | App Streamlit implementada en `notebooks/7-deploy/streamlit_app.py`. |
| Propuesta de despliegue | Cubierto | Incluida en el notebook final y como vista especifica dentro de la app. |
| Presentacion oral | Pendiente | Falta deck o guion de 10-15 minutos con demo. |

## Checklist Contra Consigna

| Requisito de la consigna | Estado | Evidencia / Ubicacion | Observaciones |
|---|---|---|---|
| Implementar una solucion funcional al problema planteado | Cubierto | `notebooks/8-reports/10-gc-entrega03_modelado_y_solucion-2026_06_03.ipynb`, `notebooks/7-deploy/streamlit_app.py` | La solucion analitica y la interfaz funcional estan implementadas. |
| Implementar modelos predictivos, descriptivos u otra tecnica justificada | Cubierto | `notebooks/5-models/07-gc-clustering-2026_04_15.ipynb`, `notebooks/5-models/08-gc-churn-2026_04_16.ipynb` | Se implemento enfoque dual: clustering + churn. |
| Describir el enfoque adoptado y justificarlo | Cubierto | Notebook 09 y notebook consolidado, secciones de enfoque dual | Clustering responde segmentacion; churn responde priorizacion de retencion. |
| Implementar modelo o sistema base | Cubierto | Notebook 07: K-Means; Notebook 08: Random Forest / Gradient Boosting | Random Forest fue seleccionado para churn. |
| Validar el modelo con metricas apropiadas | Cubierto | Notebook 07 y 08 | Clustering: Silhouette y Calinski-Harabasz. Churn: F1, AUC-ROC, matriz de confusion y classification report. |
| Analizar resultados | Cubierto | Notebook 09 y notebook consolidado | Incluye churn por segmento, revenue en riesgo y recomendaciones. |
| Reflexion critica sobre rendimiento y mejoras | Cubierto | `notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb`; notebook consolidado, secciones 12 y 13 | Incluye limitaciones del dataset, mejoras y aprendizajes. |
| Entregar notebook o equivalente | Cubierto | `notebooks/8-reports/10-gc-entrega03_modelado_y_solucion-2026_06_03.ipynb` | Notebook narrativo principal de Entrega 03. |
| Desarrollar prototipo minimo viable | Cubierto | `notebooks/7-deploy/streamlit_app.py` | App Streamlit con resumen ejecutivo, segmentos, churn, buscador, simulador y despliegue. |
| Permitir interaccion con el modelo o sistema | Cubierto | `notebooks/7-deploy/streamlit_app.py` | Permite seleccionar clientes, filtrar riesgo y estimar churn/segmento para nuevos casos. |
| Simular uso con nuevos datos | Cubierto | Vista "Simulador" de la app | Formulario de features RFM, comportamiento y preferencias de producto. |
| Incluir propuesta teorica de despliegue | Cubierto | Notebook consolidado, seccion 11; app, vista "Despliegue" | Arquitectura batch, recursos, escalabilidad y monitoreo. |
| Explicar como funcionaria en entorno real | Cubierto | Notebook consolidado, seccion 11; app, vista "Despliegue" | Propuesta batch + dashboard interno/CRM. |
| Explicar recursos requeridos | Cubierto | Notebook consolidado, seccion 11; app, vista "Despliegue" | Incluye ambiente Python, datos, almacenamiento, monitoreo y responsables. |
| Explicar alternativas para escalar | Cubierto | Notebook consolidado, seccion 11; app, vista "Despliegue" | Incluye MVP, app interna, API, feature store y retraining. |
| Presentacion oral de 10-15 minutos | Pendiente | Por crear | Falta deck o guion final. |
| Presentar problema y objetivos | Parcial | README, notebook consolidado | Debe llevarse a slides. |
| Presentar estrategia y decisiones | Parcial | Notebook consolidado | Debe llevarse a slides. |
| Demostracion en vivo o grabada del prototipo | Parcial | `notebooks/7-deploy/streamlit_app.py` | El prototipo existe; falta incorporarlo al deck o grabacion. |
| Presentar resultados y conclusiones | Parcial | Notebook 09 y notebook consolidado | Debe sintetizarse para presentacion. |
| Reflexionar sobre dificultades, aprendizajes y proximos pasos | Parcial | Notebook 09 y notebook consolidado | Debe sintetizarse para presentacion. |

## Artefactos Actuales

| Artefacto | Estado | Ubicacion |
|---|---|---|
| Notebook consolidado Entrega 03 | Creado | `notebooks/8-reports/10-gc-entrega03_modelado_y_solucion-2026_06_03.ipynb` |
| Checklist de consigna | Creado | `notebooks/8-reports/ENTREGA03_CUMPLIMIENTO.md` |
| Notebook clustering | Completo | `notebooks/5-models/07-gc-clustering-2026_04_15.ipynb` |
| Notebook churn | Completo | `notebooks/5-models/08-gc-churn-2026_04_16.ipynb` |
| Notebook interpretacion | Completo | `notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb` |
| Modelos serializados | Versionado selectivo | `data/06_models/kmeans_model.pkl`, `data/06_models/churn_model.pkl` |
| Predicciones y segmentos | Versionado selectivo | `data/07_model_output/` |
| Graficos de reporting | Versionado selectivo | `data/08_reporting/` |
| Prototipo Streamlit | Creado | `notebooks/7-deploy/streamlit_app.py` |
| Presentacion final | Pendiente | Por crear |

## Riesgos Para La Entrega

1. Sin deck o guion, la presentacion final depende demasiado de navegar notebooks en vivo.
2. La demo depende de que los artefactos livianos versionados permanezcan sincronizados con los notebooks de entrenamiento.
3. El dataset crudo sigue fuera de Git; si se quiere reproducibilidad completa, hay que documentar descarga y ejecucion de notebooks desde cero.

## Proximos Pasos Recomendados

1. Preparar deck de 10-15 minutos con problema, enfoque, resultados, demo y cierre.
2. Agregar captura de la app al notebook consolidado o al deck si se quiere evidencia visual estatica.
3. Probar la demo antes de presentar con dos clientes reales y dos simulaciones.
4. Mantener documentada la estrategia de artefactos: dataset crudo fuera de Git, outputs livianos versionados.
