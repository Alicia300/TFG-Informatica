"""
Evalúa si combinar la IA con las reglas y los enlaces mejora la detección.

Compara tres formas de decidir el nivel de riesgo, con validación cruzada
de 5 folds. "Alerta" significa nivel medio o alto.

  1. Solo IA.
  2. IA + reglas + enlaces SIN filtrar (cualquier señal sube el nivel).
  3. Diseño elegido: la IA decide, y solo un enlace de riesgo ALTO
     (por ejemplo, con dirección IP) sube el nivel a "medio".
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from analizador import analizar_contenido
from datasetPublico import RUTA_CSV, cargar_dataset, crear_modelo
from datosEntrenamiento import mensajes as mensajes_sms
from explicacion import analizar_enlaces, nivel_mas_alto


def nivel_ia(probabilidad):
    """Mismos umbrales que usa la aplicación."""

    if probabilidad >= 0.70:
        return "alto"
    if probabilidad >= 0.40:
        return "medio"
    return "bajo"


def metricas(alerta, reales):
    vp = int((alerta & (reales == 1)).sum())
    fp = int((alerta & (reales == 0)).sum())
    fn = int((~alerta & (reales == 1)).sum())

    precision = vp / (vp + fp) if vp + fp else 0
    recall = vp / (vp + fn)
    f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1, fn, fp


CONJUNTOS = {
    "SMS": ("sms", (1, 2), list(dict.fromkeys(mensajes_sms))),
    "CORREO": ("email", (1, 1), cargar_dataset(RUTA_CSV)),
}

validacion = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for nombre, (tipo, ngramas, datos) in CONJUNTOS.items():
    textos = [t for t, _ in datos]
    reales = np.array([e for _, e in datos])

    # Probabilidad de fraude de cada mensaje cuando NO se usó para entrenar.
    probabilidades = cross_val_predict(
        crear_modelo(ngramas), textos, reales,
        cv=validacion, method="predict_proba"
    )[:, 1]

    niveles_ia = [nivel_ia(p) for p in probabilidades]
    niveles_reglas = [
        analizar_contenido(t, tipo)["nivel_riesgo"] for t in textos
    ]
    niveles_enlaces = [
        nivel_mas_alto("bajo", *[e["nivel_riesgo"] for e in analizar_enlaces(t)])
        for t in textos
    ]

    variantes = {
        "1. Solo IA": niveles_ia,

        "2. IA + reglas + enlaces (sin filtrar)": [
            nivel_mas_alto(a, r, e)
            for a, r, e in zip(niveles_ia, niveles_reglas, niveles_enlaces)
        ],

        "3. Diseño elegido (enlaces de riesgo alto)": [
            nivel_mas_alto(a, "medio") if e == "alto" else a
            for a, e in zip(niveles_ia, niveles_enlaces)
        ],
    }

    print(f"\n{nombre} ({len(reales)} mensajes) - alerta = nivel medio o alto")
    print(f"{'Variante':<46}{'Prec.':>8}{'Recall':>8}{'F1':>8}{'FN':>6}{'FP':>6}")
    print("-" * 82)

    for variante, niveles in variantes.items():
        alerta = np.array([nivel != "bajo" for nivel in niveles])
        p, r, f, fn, fp = metricas(alerta, reales)
        print(f"{variante:<46}{p:>8.1%}{r:>8.1%}{f:>8.1%}{fn:>6}{fp:>6}")

print("\nFN = fraudes no detectados | FP = mensajes legítimos marcados.")