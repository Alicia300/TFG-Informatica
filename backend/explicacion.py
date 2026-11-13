"""
Funciones que explican el resultado de un análisis:
  - palabras_influyentes: qué palabras han empujado al modelo hacia "fraude".
  - extraer_urls / analizar_enlaces: enlaces escritos dentro de un mensaje.
  - nivel_mas_alto: combina varios niveles de riesgo en uno.
"""

import re
import unicodedata

from analizador import analizar_url


PATRON_URL = re.compile(r"(?:https?://|www\.)[^\s<>\"']+", re.IGNORECASE)

ORDEN_NIVELES = {"bajo": 0, "medio": 1, "alto": 2}

# Palabras muy frecuentes que no aportan información al usuario. Solo se ocultan en la explicación; el modelo sí las usa al clasificar.
PALABRAS_VACIAS = {
    "a", "al", "ante", "con", "de", "del", "el", "en", "es", "ha", "han",
    "la", "las", "lo", "los", "me", "mi", "o", "para", "por", "que", "se",
    "ser", "sera", "si", "sido", "su", "sus", "te", "tu", "tus", "un", "una",
    "y", "ya", "hola", "has", "he", "hemos", "este", "esta", "estos", "estas", "le", "les", "nos"
}


def nivel_mas_alto(*niveles):
    """Devuelve el más grave de los niveles recibidos."""

    return max(niveles, key=lambda nivel: ORDEN_NIVELES[nivel])


def extraer_urls(texto, maximo=5):
    """Busca enlaces dentro de un texto (sin repetidos)."""

    urls = []

    for coincidencia in PATRON_URL.findall(texto):
        url = coincidencia.rstrip(".,;:!?)]}»\"'")

        if url and url not in urls:
            urls.append(url)

    return urls[:maximo]


def analizar_enlaces(texto):
    """Analiza con las reglas de URL cada enlace que aparece en el texto."""

    resultados = []

    for url in extraer_urls(texto):
        analisis = analizar_url(url)
        resultados.append({
            "url": url,
            "nivel_riesgo": analisis["nivel_riesgo"],
            "indicios": analisis["indicios"]
        })

    return resultados


def _sin_acentos(texto):
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def palabras_influyentes(modelo, texto, maximo=5):
    """
    Devuelve las palabras (o pares de palabras) del texto que más han
    elevado la probabilidad de fraude según el modelo.

    Contribución de cada término = valor TF-IDF en el texto x peso que el
    modelo le asigna. Solo se devuelven las contribuciones positivas.
    """

    tfidf = modelo.named_steps["tfidf"]
    clasificador = modelo.named_steps["clasificador"]

    vector = tfidf.transform([texto]).tocoo()
    nombres = tfidf.get_feature_names_out()
    pesos = clasificador.coef_[0]

    contribuciones = sorted(
        ((nombres[j], valor * pesos[j]) for j, valor in zip(vector.col, vector.data)),
        key=lambda par: par[1],
        reverse=True
    )

    # El vectorizador quita acentos y mayúsculas: recuperamos la forma
    # original de cada palabra tal como la escribió el usuario.
    originales = {}

    for palabra in re.findall(r"\w+", texto):
        originales.setdefault(_sin_acentos(palabra.lower()), palabra.lower())

    elegidas = []
    palabras_cubiertas = set()

    for termino, contribucion in contribuciones:
        if contribucion <= 0.02 or len(elegidas) >= maximo:
            break

        partes = termino.split(" ")

        # Ignorar términos formados solo por palabras vacías.
        if all(parte in PALABRAS_VACIAS for parte in partes):
            continue

        # Evitar repetir palabras que ya aparecen en un término elegido.
        utiles = [p for p in partes if p not in PALABRAS_VACIAS]

        if all(p in palabras_cubiertas for p in utiles):
            continue

        palabras_cubiertas.update(utiles)
        elegidas.append(" ".join(originales.get(p, p) for p in partes))

    return elegidas