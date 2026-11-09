"""
Compara varios algoritmos con la MISMA validación cruzada (5 folds) y los
MISMOS datos, por separado para SMS y para correos. Después busca los
mejores parámetros de la regresión logística con GridSearchCV.

"""

import csv
import os
import time

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_validate
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from datasetPublico import RUTA_CSV, cargar_dataset
from datosEntrenamiento import mensajes as mensajes_sms


METRICAS = ["accuracy", "precision", "recall", "f1"]

# Mismos folds para todos los algoritmos: la comparación es justa.
VALIDACION = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

CARPETA = os.path.dirname(os.path.abspath(__file__))


def crear_tfidf():
    return TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2)
    )


# Algoritmos a comparar (todos reciben el mismo texto vectorizado).
ALGORITMOS = {
    "Regresión logística (C=10)": LogisticRegression(
        C=10, max_iter=1000, random_state=42
    ),
    "Naive Bayes": MultinomialNB(),
    "SVM lineal": LinearSVC(random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, random_state=42, n_jobs=-1
    ),
}


def comparar_algoritmos(nombre_dataset, datos):
    """Evalúa cada algoritmo y devuelve las filas de la tabla."""

    textos = [t for t, _ in datos]
    etiquetas = [e for _, e in datos]

    print(f"\n{'=' * 72}")
    print(f"COMPARACIÓN DE ALGORITMOS - {nombre_dataset} ({len(datos)} mensajes)")
    print("=" * 72)
    print(f"{'Algoritmo':<28}{'Exact.':>8}{'Prec.':>8}{'Recall':>8}"
          f"{'F1':>8}{'Seg.':>8}")
    print("-" * 72)

    filas = []

    for nombre, clasificador in ALGORITMOS.items():
        modelo = Pipeline([
            ("tfidf", crear_tfidf()),
            ("clasificador", clasificador)
        ])

        inicio = time.time()
        res = cross_validate(
            modelo, textos, etiquetas,
            cv=VALIDACION, scoring=METRICAS
        )
        segundos = time.time() - inicio

        medias = {m: res[f"test_{m}"].mean() for m in METRICAS}

        print(f"{nombre:<28}{medias['accuracy']:>8.1%}{medias['precision']:>8.1%}"
              f"{medias['recall']:>8.1%}{medias['f1']:>8.1%}{segundos:>8.1f}")

        filas.append([nombre_dataset, nombre] + [round(medias[m], 4) for m in METRICAS])

    return filas


def ajustar_regresion_logistica(nombre_dataset, datos):
    """Busca la mejor combinación de parámetros con GridSearchCV."""

    textos = [t for t, _ in datos]
    etiquetas = [e for _, e in datos]

    modelo = Pipeline([
        ("tfidf", crear_tfidf()),
        ("clasificador", LogisticRegression(max_iter=1000, random_state=42))
    ])

    parametros = {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "clasificador__C": [0.1, 1, 10, 100],
    }

    busqueda = GridSearchCV(
        modelo, parametros,
        cv=VALIDACION, scoring=METRICAS, refit="f1", n_jobs=-1
    )
    busqueda.fit(textos, etiquetas)

    r = busqueda.cv_results_
    orden = sorted(range(len(r["params"])), key=lambda i: -r["mean_test_f1"][i])

    print(f"\nAJUSTE DE PARÁMETROS (regresión logística) - {nombre_dataset}")
    print("-" * 72)
    print(f"{'ngramas':<10}{'C':>7}{'Exact.':>9}{'Prec.':>8}{'Recall':>8}{'F1':>8}")

    for i in orden:
        p = r["params"][i]
        print(f"{str(p['tfidf__ngram_range']):<10}{p['clasificador__C']:>7}"
              f"{r['mean_test_accuracy'][i]:>9.1%}{r['mean_test_precision'][i]:>8.1%}"
              f"{r['mean_test_recall'][i]:>8.1%}{r['mean_test_f1'][i]:>8.1%}")

    print(f"\nMejor combinación según F1: {busqueda.best_params_}")


if __name__ == "__main__":
    conjuntos = {
        "SMS": list(dict.fromkeys(mensajes_sms)),
        "CORREO": cargar_dataset(RUTA_CSV),
    }

    todas_las_filas = []

    for nombre, datos in conjuntos.items():
        todas_las_filas += comparar_algoritmos(nombre, datos)

    for nombre, datos in conjuntos.items():
        ajustar_regresion_logistica(nombre, datos)

    # Guardar la tabla para la memoria (se abre bien con Excel).
    ruta_csv = os.path.join(CARPETA, "resultados_comparacion.csv")

    with open(ruta_csv, "w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo, delimiter=";")
        escritor.writerow(["Conjunto", "Algoritmo"] + METRICAS)
        escritor.writerows(todas_las_filas)

    print(f"\nTabla guardada en: {ruta_csv}")