"""
Entrena los dos modelos de la aplicación y los guarda en backend/modelos/.

  - modelo_sms.joblib   -> entrenado con el conjunto de SMS del proyecto.
  - modelo_email.joblib -> entrenado con el dataset público SpaPhish.

"""

import os

import joblib
from sklearn.model_selection import StratifiedKFold, cross_validate

from datasetPublico import RUTA_CSV, cargar_dataset, crear_modelo
from datosEntrenamiento import mensajes as mensajes_sms


# Configuración de cada modelo: la combinación con mejor F1 en el ajuste de
# parámetros (GridSearchCV) de compararModelos.py.
# ngramas (1, 1) = palabras sueltas; (1, 2) = palabras sueltas y pares.
CONFIGURACION = {
    "sms": {"ngramas": (1, 1), "C": 100},
    "email": {"ngramas": (1, 1), "C": 10},
}

CARPETA_MODELOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "modelos"
)


def entrenar_y_guardar(nombre, datos):
    """Evalúa con validación cruzada, entrena con todo y guarda el modelo."""

    textos = [t for t, _ in datos]
    etiquetas = [e for _, e in datos]

    # Evaluación rápida para dejar constancia del rendimiento.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    res = cross_validate(
        crear_modelo(**CONFIGURACION[nombre]), textos, etiquetas, cv=cv,
        scoring=["accuracy", "precision", "recall", "f1"]
    )

    print(f"\nModelo {nombre.upper()} ({len(datos)} mensajes)")
    for metrica in ["accuracy", "precision", "recall", "f1"]:
        print(f"  {metrica:<10} {res[f'test_{metrica}'].mean():.2%}")

    # Entrenamiento final con todos los datos y guardado.
    modelo = crear_modelo(**CONFIGURACION[nombre])
    modelo.fit(textos, etiquetas)

    os.makedirs(CARPETA_MODELOS, exist_ok=True)
    ruta = os.path.join(CARPETA_MODELOS, f"modelo_{nombre}.joblib")
    joblib.dump(modelo, ruta, compress=3)

    peso = os.path.getsize(ruta) / (1024 * 1024)
    print(f"  Guardado en {ruta} ({peso:.1f} MB)")


if __name__ == "__main__":
    if not os.path.exists(RUTA_CSV):
        raise SystemExit(
            f"No se encuentra {RUTA_CSV}. El conjunto SpaPhish debe "
            "guardarse como backend/datos/spaphish.csv (ver README)."
        )

    entrenar_y_guardar("sms", list(dict.fromkeys(mensajes_sms)))
    entrenar_y_guardar("email", cargar_dataset(RUTA_CSV))