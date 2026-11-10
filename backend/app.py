from flask import Flask, render_template, request, jsonify

from analizador import analizar_contenido
from explicacion import analizar_enlaces
from modeloIA import clasificar_mensaje, palabras_clave

app = Flask(__name__)

# Umbrales de probabilidad de "sospechoso" para asignar el nivel de riesgo.
UMBRAL_ALTO = 0.70
UMBRAL_MEDIO = 0.40


def obtener_recomendaciones(tipo, nivel_riesgo):
    """Genera recomendaciones preventivas según el tipo y el riesgo."""

    if nivel_riesgo == "alto":
        if tipo == "url":
            return [
                "No abras el enlace si no conoces su procedencia.",
                "No introduzcas contraseñas ni datos personales.",
                "Accede a la página oficial escribiendo su dirección directamente.",
                "Si el enlace suplanta a una empresa, contacta con ella por sus canales oficiales."
            ]

        return [
            "No respondas al mensaje ni sigas sus instrucciones.",
            "No abras los enlaces ni descargues archivos adjuntos.",
            "No facilites contraseñas, códigos de verificación ni datos bancarios.",
            "Comprueba la información contactando con la entidad por sus canales oficiales."
        ]

    elif nivel_riesgo == "medio":
        if tipo == "url":
            return [
                "Comprueba que el dominio corresponde a la página que esperas visitar.",
                "Evita introducir datos personales hasta verificar la dirección.",
                "Desconfía de los enlaces acortados o con direcciones poco habituales."
            ]

        return [
            "Comprueba quién ha enviado el mensaje.",
            "Verifica la información mediante los canales oficiales de la entidad.",
            "No compartas datos personales o bancarios sin comprobar la solicitud."
        ]

    else:
        if tipo == "url":
            return [
                "Comprueba que la dirección pertenece al sitio web que deseas visitar.",
                "Evita introducir información personal si tienes dudas sobre la página."
            ]

        return [
            "Comprueba que reconoces al remitente.",
            "Desconfía de solicitudes inesperadas de información personal.",
            "Recuerda que un resultado de bajo riesgo no garantiza que el mensaje sea seguro."
        ]


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/analizar", methods=["POST"])
def analizar():

    # Comprobamos que la petición contiene un JSON válido.
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "La petición debe contener datos en formato JSON."
        }), 400

    # Comprobamos que el contenido sea una cadena de texto.
    contenido = datos.get("contenido")

    if not isinstance(contenido, str) or not contenido.strip():
        return jsonify({
            "error": "Debes introducir contenido para analizar."
        }), 400

    contenido = contenido.strip()

    # Obtenemos y validamos el tipo de contenido.
    tipo = datos.get("tipo", "sms")

    if not isinstance(tipo, str) or tipo not in ("url", "sms", "email"):
        return jsonify({
            "error": "El tipo de contenido no es válido."
        }), 400

    # Análisis de direcciones URL mediante reglas.
    if tipo == "url":
        resultado = analizar_contenido(contenido, tipo)

    # Clasificación de SMS y correos mediante inteligencia artificial.
    else:
        resultado_ia = clasificar_mensaje(contenido, tipo)

        clasificacion = resultado_ia["clasificacion"]
        confianza = resultado_ia["confianza_sospechoso"]

        # Determinamos el nivel de riesgo según la probabilidad.
        if confianza >= UMBRAL_ALTO:
            nivel_riesgo = "alto"
            indicios = [
                "El modelo de IA ha identificado patrones "
                "compatibles con un mensaje sospechoso."
            ]

        elif confianza >= UMBRAL_MEDIO:
            nivel_riesgo = "medio"
            indicios = [
                "El modelo de IA ha detectado algunos patrones "
                "que podrían indicar un mensaje sospechoso."
            ]

        else:
            nivel_riesgo = "bajo"
            indicios = []

        # Enlaces escritos dentro del mensaje. Se analizan con las reglas
        # de URL. Normalmente solo explican el resultado, pero un enlace de
        # riesgo alto (por ejemplo, con una dirección IP) es algo que el
        # modelo de texto no puede ver, así que sube el nivel a "medio".
        enlaces = analizar_enlaces(contenido)

        if any(e["nivel_riesgo"] == "alto" for e in enlaces):
            if nivel_riesgo == "bajo":
                nivel_riesgo = "medio"

            indicios.append(
                "El mensaje contiene un enlace con señales de riesgo alto."
            )

        # Explicación del resultado: solo si hay algo que explicar.
        palabras = []

        if nivel_riesgo != "bajo":
            palabras = palabras_clave(contenido, tipo)

            # Señales concretas de las reglas (urgencia, petición de
            # datos, premios). El aviso genérico de "enlace" se omite
            # porque ya se muestra en la sección de enlaces.
            reglas = analizar_contenido(contenido, tipo)

            for indicio in reglas["indicios"]:
                if "enlace" not in indicio.lower():
                    indicios.append(indicio)

        resultado = {
            "nivel_riesgo": nivel_riesgo,
            "puntuacion": round(confianza * 100),
            "indicios": indicios,
            "numero_indicios": len(indicios),
            "palabras_influyentes": palabras,
            "enlaces": enlaces,
            "clasificacion_ia": clasificacion,
            "confianza_sospechoso": confianza
        }

    resultado["recomendaciones"] = obtener_recomendaciones(
        tipo,
        resultado["nivel_riesgo"]
    )

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)