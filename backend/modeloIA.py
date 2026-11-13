import os
import joblib
from explicacion import palabras_influyentes

CARPETA_MODELOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "modelos"
)

RUTAS_MODELOS = {
    "sms": os.path.join(CARPETA_MODELOS, "modelo_sms.joblib"),
    "email": os.path.join(CARPETA_MODELOS, "modelo_email.joblib"),
}


def _cargar_modelos():
    """Carga los modelos entrenados al arrancar la aplicación."""

    modelos = {}

    for tipo, ruta in RUTAS_MODELOS.items():
        if not os.path.exists(ruta):
            raise FileNotFoundError(
                f"No se encuentra el modelo '{tipo}' ({ruta}). "
                "Es necesario ejecutar antes: python entrenar.py"
            )
        modelos[tipo] = joblib.load(ruta)

    return modelos


MODELOS = _cargar_modelos()


def clasificar_mensaje(texto, tipo="sms"):
    """Clasifica un SMS o un correo como legítimo o sospechoso."""

    if tipo not in MODELOS:
        raise ValueError(f"Tipo de mensaje no válido: {tipo}")

    modelo = MODELOS[tipo]
    probabilidades = modelo.predict_proba([texto])[0]

    indice_sospechoso = list(
        modelo.named_steps["clasificador"].classes_
    ).index(1)

    confianza = float(probabilidades[indice_sospechoso])

    return {
        "clasificacion": (
            "sospechoso" if confianza >= 0.5 else "legitimo"
        ),
        "confianza_sospechoso": round(confianza, 4)
    }


def palabras_clave(texto, tipo="sms", maximo=5):
    """Palabras del texto que más han elevado el riesgo según el modelo."""

    return palabras_influyentes(MODELOS[tipo], texto, maximo)


if __name__ == "__main__":
    # Mensajes nuevos para realizar pruebas manuales: (tipo, texto, esperado).
    ejemplos = [
        ("sms", "Tu envío llegará mañana entre las diez y las doce.", "legitimo"),
        ("sms", "Comparte el código recibido por SMS para desbloquear tu cuenta.", "sospechoso"),
        ("sms", "Hola, ¿te viene bien quedar el viernes por la tarde?", "legitimo"),
        ("sms", "Tu cuenta bancaria será suspendida si no confirmas tus datos ahora.", "sospechoso"),
        ("sms", "Introduce el número de tu tarjeta para recibir un reembolso urgente.", "sospechoso"),
        ("sms", "La reunión se ha cambiado a las nueve de la mañana.", "legitimo"),
        (
            "email",
            "Asunto: Reunión del jueves. Hola a todos, os confirmo que la reunión "
            "del proyecto será el jueves a las 10:00 en la sala 3. Adjunto el orden "
            "del día. Un saludo, Marta.",
            "legitimo"
        ),
        (
            "email",
            "Asunto: Aviso de seguridad. Estimado cliente, hemos detectado un acceso "
            "no autorizado a su cuenta bancaria. Para evitar el bloqueo definitivo, "
            "verifique su identidad en el siguiente enlace en las próximas 24 horas: "
            "http://banco-seguro-verificacion.example/login",
            "sospechoso"
        ),
    ]

    print("PRUEBAS MANUALES DE LOS MODELOS DE IA")
    print("=" * 55)

    for tipo, texto, esperado in ejemplos:
        resultado = clasificar_mensaje(texto, tipo)

        print(f"\n[{tipo.upper()}] {texto[:90]}")
        print(f"Esperado: {esperado} | Obtenido: {resultado['clasificacion']} "
              f"({resultado['confianza_sospechoso']:.1%})")
        print("Resultado de la prueba:",
              "CORRECTO" if resultado["clasificacion"] == esperado else "INCORRECTO")