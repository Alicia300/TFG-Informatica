from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from datosEntrenamiento import mensajes


# Separar los textos de sus etiquetas.
textos = [texto for texto, etiqueta in mensajes]
etiquetas = [etiqueta for texto, etiqueta in mensajes]


# Crear el modelo: TF-IDF + Regresión Logística.
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
            C=10,  # Menos regularización: probabilidades más definidas.
            max_iter=1000,
            random_state=42
        )
    )
])


# Entrenar el modelo con los ejemplos disponibles.
modelo.fit(textos, etiquetas)


def clasificar_mensaje(texto):
    """Clasifica un mensaje como legítimo o sospechoso."""

    prediccion = int(modelo.predict([texto])[0])
    probabilidades = modelo.predict_proba([texto])[0]

    indice_sospechoso = list(
        modelo.named_steps["clasificador"].classes_
    ).index(1)

    confianza = float(probabilidades[indice_sospechoso])

    return {
        "clasificacion": (
            "sospechoso" if prediccion == 1 else "legitimo"
        ),
        "confianza_sospechoso": round(confianza, 4)
    }


if __name__ == "__main__":
    # Mensajes nuevos para realizar pruebas manuales.
    ejemplos = [
        (
            "Tu envío llegará mañana entre las diez y las doce.",
            "legitimo"
        ),
        (
            "Comparte el código recibido por SMS para desbloquear tu cuenta.",
            "sospechoso"
        ),
        (
            "Hola, ¿te viene bien quedar el viernes por la tarde?",
            "legitimo"
        ),
        (
            "Tu cuenta bancaria será suspendida si no confirmas tus datos ahora.",
            "sospechoso"
        ),
        (
            "Puedes consultar el estado de tu pedido en la aplicación oficial.",
            "legitimo"
        ),
        (
            "Introduce el número de tu tarjeta para recibir un reembolso urgente.",
            "sospechoso"
        ),
        (
            "La reunión se ha cambiado a las nueve de la mañana.",
            "legitimo"
        ),
        (
            "Has ganado un premio, paga los gastos para poder recibirlo.",
            "sospechoso"
        )
    ]

    print("PRUEBAS MANUALES DEL MODELO DE IA")
    print("=" * 55)

    for texto, etiqueta_esperada in ejemplos:
        resultado = clasificar_mensaje(texto)

        clasificacion = resultado["clasificacion"]
        confianza = resultado["confianza_sospechoso"]

        print(f"\nMensaje: {texto}")
        print(f"Clasificación esperada: {etiqueta_esperada}")
        print(f"Clasificación obtenida: {clasificacion}")
        print(
            "Puntuación estimada de sospecha: "
            f"{confianza:.1%}"
        )

        if clasificacion == etiqueta_esperada:
            print("Resultado de la prueba: CORRECTO")
        else:
            print("Resultado de la prueba: INCORRECTO")