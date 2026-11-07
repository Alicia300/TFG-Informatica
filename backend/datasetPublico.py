
#Experimentos con un dataset público de correos en español (SpaPhish).

import csv
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline

from datosEntrenamiento import mensajes as mensajes_propios

RUTA_CSV = "datos/spaphish.csv"
SEPARADOR = ","            # El README dice ";", pero el CSV real usa comas.
COLUMNA_ASUNTO = "subject"    # Pon None si el CSV no tiene asunto.
COLUMNA_CUERPO = "body"
COLUMNA_ETIQUETA = "Label"
VALOR_FRAUDE = "1"            # Valor de la etiqueta que indica phishing.
LONGITUD_MAXIMA = 1500        # Se recorta cada correo para acelerar.


def cargar_dataset(ruta):
    """Lee el CSV y devuelve una lista de (texto, etiqueta)."""

    csv.field_size_limit(10_000_000)

    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=SEPARADOR)
        columnas = lector.fieldnames or []

        necesarias = [COLUMNA_CUERPO, COLUMNA_ETIQUETA]
        if COLUMNA_ASUNTO:
            necesarias.append(COLUMNA_ASUNTO)

        faltan = [c for c in necesarias if c not in columnas]
        if faltan:
            print(f"No se encuentran las columnas: {faltan}")
            print(f"Columnas disponibles en el CSV: {columnas}")
            print("Corrige las constantes de CONFIGURACIÓN y vuelve a ejecutar.")
            sys.exit(1)

        datos = []

        for fila in lector:
            asunto = (fila.get(COLUMNA_ASUNTO) or "") if COLUMNA_ASUNTO else ""
            cuerpo = fila.get(COLUMNA_CUERPO) or ""
            texto = f"{asunto}. {cuerpo}".strip(". ").strip()[:LONGITUD_MAXIMA]

            if not texto:
                continue

            etiqueta = 1 if str(fila[COLUMNA_ETIQUETA]).strip() == VALOR_FRAUDE else 0
            datos.append((texto, etiqueta))

    # Eliminar repetidos.
    return list(dict.fromkeys(datos))


def crear_modelo():

    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2)
        )),
        ("clasificador", LogisticRegression(
            C=10,
            max_iter=1000,
            random_state=42
        ))
    ])


def validacion_cruzada(datos, titulo):
    textos = [t for t, _ in datos]
    etiquetas = [e for _, e in datos]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    res = cross_validate(
        crear_modelo(), textos, etiquetas, cv=cv,
        scoring=["accuracy", "precision", "recall", "f1"]
    )

    print(f"\n{titulo}")
    print(f"Mensajes: {len(datos)} "
          f"(fraude: {sum(etiquetas)}, legítimos: {len(etiquetas) - sum(etiquetas)})")
    print("-" * 60)

    for metrica in ["accuracy", "precision", "recall", "f1"]:
        v = res[f"test_{metrica}"]
        print(f"{metrica:<10} {v.mean():.2%} (± {v.std():.2%})")


def evaluar_sobre_propios(publico, usar_publico):

    textos = [t for t, _ in mensajes_propios]
    etiquetas = [e for _, e in mensajes_propios]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    reales, predichas = [], []

    for idx_ent, idx_prueba in cv.split(textos, etiquetas):
        ent_x = [textos[i] for i in idx_ent]
        ent_y = [etiquetas[i] for i in idx_ent]

        if usar_publico:
            ent_x += [t for t, _ in publico]
            ent_y += [e for _, e in publico]

        modelo = crear_modelo()
        modelo.fit(ent_x, ent_y)

        reales += [etiquetas[i] for i in idx_prueba]
        predichas += list(modelo.predict([textos[i] for i in idx_prueba]))

    informe = classification_report(
        reales, predichas, labels=[0, 1], output_dict=True, zero_division=0
    )
    matriz = confusion_matrix(reales, predichas, labels=[0, 1])

    return {
        "accuracy": informe["accuracy"],
        "precision": informe["1"]["precision"],
        "recall": informe["1"]["recall"],
        "f1": informe["1"]["f1-score"],
        "fn": int(matriz[1][0]),
        "fp": int(matriz[0][1]),
    }


if __name__ == "__main__":
    publico = cargar_dataset(RUTA_CSV)

    # Experimento A: el dataset público por sí solo.
    validacion_cruzada(publico, "A) VALIDACIÓN CRUZADA: dataset público")

    # Experimento B: entrenar con el público y probar con tus mensajes.
    # Mide si el modelo generaliza a un tipo de texto distinto.
    modelo = crear_modelo()
    modelo.fit([t for t, _ in publico], [e for _, e in publico])

    textos_propios = [t for t, _ in mensajes_propios]
    etiquetas_propias = [e for _, e in mensajes_propios]
    predicciones = modelo.predict(textos_propios)

    print("\nB) ENTRENADO CON EL PÚBLICO, PROBADO CON TUS MENSAJES")
    print("-" * 60)
    print(classification_report(
        etiquetas_propias, predicciones,
        labels=[0, 1], target_names=["Legítimo", "Sospechoso"],
        zero_division=0
    ))
    print("Matriz de confusión:")
    print(confusion_matrix(etiquetas_propias, predicciones, labels=[0, 1]))

    # Experimento C: todo junto.
    validacion_cruzada(
        publico + list(mensajes_propios),
        "C) VALIDACIÓN CRUZADA: dataset público + tus mensajes"
    )

    # Experimento D: ¿ayuda SpaPhish con tus mensajes cortos?
    print("\nD) RESULTADO SOBRE TUS MENSAJES (validación cruzada)")
    print("-" * 60)
    print(f"{'Entrenamiento':<28}{'Exact.':>8}{'Prec.':>8}{'Recall':>8}"
          f"{'F1':>8}{'FN':>5}{'FP':>5}")

    for nombre, usar in [("Solo tus mensajes", False),
                         ("Tus mensajes + SpaPhish", True)]:
        r = evaluar_sobre_propios(publico, usar)
        print(f"{nombre:<28}{r['accuracy']:>8.1%}{r['precision']:>8.1%}"
              f"{r['recall']:>8.1%}{r['f1']:>8.1%}{r['fn']:>5}{r['fp']:>5}")