
import re
import ipaddress
from urllib.parse import urlparse


def calcular_riesgo(indicios, puntuacion):
    """Devuelve un resultado uniforme para todos los análisis."""

    if puntuacion == 0:
        nivel_riesgo = "bajo"
    elif puntuacion == 1:
        nivel_riesgo = "medio"
    else:
        nivel_riesgo = "alto"

    return {
        "nivel_riesgo": nivel_riesgo,
        "puntuacion": puntuacion,
        "indicios": indicios,
        "numero_indicios": len(indicios)
    }


def analizar_url(contenido):
    """Analiza una URL mediante reglas heurísticas."""

    texto = contenido.strip()
    indicios = []
    puntuacion = 0

    # Añadir el protocolo si el usuario no lo ha escrito.
    direccion_texto = texto

    if not direccion_texto.lower().startswith(
        ("http://", "https://")
    ):
        direccion_texto = "https://" + direccion_texto

    try:
        direccion = urlparse(direccion_texto)
        dominio = direccion.hostname

        # Comprobar que el puerto, si existe, tiene un formato válido.
        _ = direccion.port

        if not dominio:
            raise ValueError("No se ha encontrado un dominio válido.")

    except ValueError:
        return calcular_riesgo(
            ["La dirección no tiene un formato válido."],
            2
        )

    dominio = dominio.lower()

    # 1. HTTP sin cifrado: 1 punto.
    if direccion.scheme.lower() == "http":
        indicios.append(
            "El enlace utiliza HTTP sin cifrado HTTPS."
        )
        puntuacion += 1

    # 2. Dirección IP como dominio: 2 puntos.
    try:
        ipaddress.ip_address(dominio)
        es_direccion_ip = True
    except ValueError:
        es_direccion_ip = False

    if es_direccion_ip:
        indicios.append(
            "El enlace utiliza una dirección IP en lugar de un dominio."
        )
        puntuacion += 2

    # 3. Carácter @ en la autoridad de la URL: 2 puntos.
    if "@" in direccion.netloc:
        indicios.append(
            "La dirección contiene '@', que puede ocultar el destino real."
        )
        puntuacion += 2

    # 4. Servicios conocidos de acortamiento: 1 punto.
    acortadores = {
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd",
        "cutt.ly",
        "rebrand.ly"
    }

    if dominio in acortadores:
        indicios.append(
            "El enlace utiliza un servicio de acortamiento de URL."
        )
        puntuacion += 1

    # 5. Términos asociados con accesos o verificaciones: 1 punto.
    palabras_sospechosas = [
        "login",
        "verify",
        "verificacion",
        "secure",
        "account",
        "signin",
        "update"
    ]

    etiquetas_dominio = dominio.split(".")

    if any(
        palabra in etiqueta
        for etiqueta in etiquetas_dominio
        for palabra in palabras_sospechosas
    ):
        indicios.append(
            "El dominio contiene términos asociados con accesos "
            "o verificaciones."
        )
        puntuacion += 1

    return calcular_riesgo(indicios, puntuacion)


def analizar_contenido(contenido, tipo="sms"):
    """Analiza SMS, correos electrónicos o enlaces."""

    if tipo == "url":
        return analizar_url(contenido)

    texto = contenido.lower()
    indicios = []
    puntuacion = 0

    # 1. Expresiones de urgencia: 1 punto.
    expresiones_urgencia = [
        "actúa inmediatamente",
        "actua inmediatamente",
        "último aviso",
        "ultimo aviso",
        "urgente",
        "inmediatamente",
        "en las próximas 24 horas",
        "en las proximas 24 horas"
    ]

    if any(
        expresion in texto
        for expresion in expresiones_urgencia
    ):
        indicios.append(
            "El mensaje utiliza expresiones de urgencia."
        )
        puntuacion += 1

    # 2. Solicitud de datos o credenciales: 2 puntos.
    expresiones_datos = [
        "confirma tu contraseña",
        "confirma tu contrasena",
        "verifica tu cuenta",
        "verifique su cuenta",
        "introduce tu contraseña",
        "introduce tu contrasena",
        "facilita tus datos",
        "datos bancarios"
    ]

    if any(
        expresion in texto
        for expresion in expresiones_datos
    ):
        indicios.append(
            "El mensaje solicita verificar una cuenta "
            "o proporcionar datos."
        )
        puntuacion += 2

    # 3. Premios inesperados: 1 punto.
    expresiones_premios = [
        "has ganado un premio",
        "ha ganado un premio",
        "has sido seleccionado",
        "premio gratis",
        "reclama tu premio"
    ]

    if any(
        expresion in texto
        for expresion in expresiones_premios
    ):
        indicios.append(
            "El mensaje anuncia un premio o recompensa inesperada."
        )
        puntuacion += 2

    # 4. Presencia de enlaces: 1 punto.
    patron_url = r"https?://|www\."

    if re.search(patron_url, texto):
        indicios.append(
            "El mensaje contiene un enlace que conviene comprobar."
        )
        puntuacion += 1

    return calcular_riesgo(indicios, puntuacion)