from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from datosEntrenamiento import mensajes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# Separar los textos y sus etiquetas.
textos = [texto for texto, etiqueta in mensajes]
etiquetas = [etiqueta for texto, etiqueta in mensajes]


# Reservar ejemplos para evaluar el modelo.
textos_entrenamiento, textos_prueba, etiquetas_entrenamiento, etiquetas_prueba = (
    train_test_split(
        textos,
        etiquetas,
        test_size=0.25,
        random_state=42,
        stratify=etiquetas
    )
)


# Crear el modelo.
modelo = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2)
        )
    ),
    (
        "clasificador",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )
])


# Entrenar solo con los ejemplos de entrenamiento.
modelo.fit(textos_entrenamiento, etiquetas_entrenamiento)


# Evaluar con los ejemplos reservados.
predicciones = modelo.predict(textos_prueba)

print("EVALUACIÓN INICIAL DE LA IA")
print("-" * 45)

print(f"Mensajes para entrenar: {len(textos_entrenamiento)}")
print(f"Mensajes para evaluar: {len(textos_prueba)}")

exactitud = accuracy_score(etiquetas_prueba, predicciones)
print(f"\nExactitud: {exactitud:.2%}")

print("\nInforme de clasificación:")
print(
    classification_report(
        etiquetas_prueba,
        predicciones,
        labels=[0, 1],
        target_names=["Legítimo", "Sospechoso"],
        zero_division=0
    )
)

print("Matriz de confusión:")
print(
    confusion_matrix(
        etiquetas_prueba,
        predicciones,
        labels=[0, 1]
    )
)


# Mostrar los mensajes clasificados incorrectamente.
print("\nMENSAJES CLASIFICADOS INCORRECTAMENTE")
print("-" * 45)

errores = 0

for texto, etiqueta_real, prediccion in zip(
    textos_prueba,
    etiquetas_prueba,
    predicciones
):
    if etiqueta_real != prediccion:
        errores += 1

        clase_real = (
            "Legítimo" if etiqueta_real == 0 else "Sospechoso"
        )

        clase_predicha = (
            "Legítimo" if prediccion == 0 else "Sospechoso"
        )

        print(f"\nMensaje: {texto}")
        print(f"Clasificación real: {clase_real}")
        print(f"Clasificación de la IA: {clase_predicha}")

if errores == 0:
    print("No se han encontrado errores en esta evaluación.")
else:
    print(f"\nTotal de errores: {errores}")