
from analizador import analizar_contenido


# Cada caso contiene el tipo, el texto y la clasificación esperada.
casos_prueba = [
    {
        "tipo": "sms",
        "contenido": "Hola, ¿quedamos mañana?",
        "esperado": "bajo"
    },
    {
        "tipo": "sms",
        "contenido": "URGENTE: confirma tu contraseña",
        "esperado": "alto"
    },
    {
        "tipo": "email",
        "contenido": "Confirma tu contraseña",
        "esperado": "alto"
    },
    {
        "tipo": "email",
        "contenido": "Tu pedido ha sido enviado correctamente",
        "esperado": "bajo"
    },
    {
        "tipo": "url",
        "contenido": "http://example.com",
        "esperado": "medio"
    },
    {
        "tipo": "url",
        "contenido": "http://192.0.2.1/login",
        "esperado": "alto"
    },
    {
        "tipo": "sms",
        "contenido": "Has ganado un premio gratis",
        "esperado": "alto"
    },
    {
        "tipo": "email",
        "contenido": "La reunión será mañana a las diez",
        "esperado": "bajo"
    }
]


aciertos = 0

print("EVALUACIÓN DEL ANALIZADOR")
print("-" * 95)
print(f"{'Caso':<6}{'Tipo':<7}{'Esperado':<10}{'Obtenido':<10}"
      f"{'Punt.':<7}{'Resultado':<11}Contenido")
print("-" * 95)

for numero, caso in enumerate(casos_prueba, start=1):
    resultado = analizar_contenido(caso["contenido"], caso["tipo"])

    esperado = caso["esperado"]
    obtenido = resultado["nivel_riesgo"]
    correcto = esperado == obtenido

    if correcto:
        aciertos += 1

    estado = "CORRECTO" if correcto else "ERROR"

    print(f"{numero:<6}{caso['tipo']:<7}{esperado:<10}{obtenido:<10}"
          f"{resultado['puntuacion']:<7}{estado:<11}{caso['contenido']}")

total = len(casos_prueba)

print("-" * 95)
print(f"Aciertos: {aciertos}/{total} ({aciertos / total:.1%})")